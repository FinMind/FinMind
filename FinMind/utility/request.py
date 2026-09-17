import asyncio
import concurrent.futures
import hashlib
import os
import ssl
import time
from typing import Dict, List, Union

import nest_asyncio
import requests
from loguru import logger
from tqdm import tqdm

nest_asyncio.apply()


def request_get(
    session: requests.Session,
    url: str,
    params: Dict[str, Union[int, str, float]] = None,
    timeout: int = 60,
    max_retry_times: int = 10,
    verbose: bool = False,
):
    """
    單次 request，支援 retry 與 log
    """
    response = None
    for retry_times in range(1, max_retry_times + 1):
        try:
            response = session.get(
                url,
                verify=True,
                params=params,
                timeout=timeout,
            )
            if response.status_code == 504:
                if verbose:
                    logger.warning(
                        f"status_code=504, retry {retry_times}/{max_retry_times}"
                    )
                time.sleep(retry_times * 0.1)
            else:
                break
        except (
            requests.ConnectionError,
            ssl.SSLError,
            requests.exceptions.ReadTimeout,
            requests.exceptions.ChunkedEncodingError,
        ) as exc:
            if verbose:
                logger.warning(
                    f"Error: {exc}, retry {retry_times}/{max_retry_times}"
                )
            time.sleep(retry_times * 0.1)
        except Exception as exc:
            if verbose:
                logger.warning(
                    f"Unexpected error: {exc}, retry {retry_times}/{max_retry_times}"
                )
            time.sleep(retry_times * 0.1)
    if response and response.status_code != 200:
        raise Exception(
            f"Final response status: {response.status_code}, text: {response.text}"
        )
    return response


RETRYABLE_ERRORS = (
    requests.ConnectionError,
    ssl.SSLError,
    requests.exceptions.ReadTimeout,
    requests.exceptions.ChunkedEncodingError,
)
REDIRECT_STATUS = (301, 302, 303, 307, 308)


def download_storage_object(
    session: requests.Session,
    url: str,
    params: Dict[str, Union[int, str, float]] = None,
    timeout: int = 60,
    max_retry_times: int = 10,
    verbose: bool = False,
) -> bytes:
    """
    下載整日資料物件，傳輸中斷時以 Range + If-Match 續傳

    storage_objects 回 307 導向有效期限約 3 分鐘的下載網址，
    所以每次（含重試）都重新取得網址；已收到的內容保留，
    只要求剩下的位元組，並以 If-Match 確認仍是同一版本，
    版本不同（412）才從頭下載。完成後檢查長度，ETag 不含 "-" 時再比對 MD5。
    """
    buffer = bytearray()
    etag = None
    total = None
    for retry_times in range(1, max_retry_times + 1):
        try:
            response = session.get(
                url,
                verify=True,
                params=params,
                timeout=timeout,
                allow_redirects=False,
            )
        except RETRYABLE_ERRORS as exc:
            if verbose:
                logger.warning(
                    f"Error: {exc}, retry {retry_times}/{max_retry_times}"
                )
            time.sleep(retry_times * 0.5)
            continue
        if response.status_code == 200:
            return response.content
        if response.status_code == 504:
            time.sleep(retry_times * 0.5)
            continue
        if response.status_code not in REDIRECT_STATUS:
            raise Exception(
                f"Final response status: {response.status_code}, text: {response.text}"
            )
        object_url = response.headers["Location"]

        headers = {}
        if buffer and etag:
            headers = {"Range": f"bytes={len(buffer)}-", "If-Match": etag}
        try:
            # 下載網址本身帶簽章，不能帶 session 的 Authorization header
            with requests.get(
                object_url, headers=headers, stream=True, timeout=timeout
            ) as object_response:
                status_code = object_response.status_code
                if status_code == 200:
                    buffer = bytearray()
                    etag = object_response.headers.get("ETag")
                    content_length = object_response.headers.get(
                        "Content-Length"
                    )
                    total = int(content_length) if content_length else None
                elif status_code == 412:
                    # 物件在兩次請求之間已更新，已收到的內容作廢
                    buffer, etag, total = bytearray(), None, None
                    continue
                elif status_code != 206:
                    if verbose:
                        logger.warning(
                            f"status_code={status_code}, retry {retry_times}/{max_retry_times}"
                        )
                    time.sleep(retry_times * 0.5)
                    continue
                for chunk in object_response.iter_content(chunk_size=1 << 20):
                    buffer.extend(chunk)
        except RETRYABLE_ERRORS as exc:
            if verbose:
                logger.warning(
                    f"Download interrupted at {len(buffer)} bytes: {exc}, "
                    f"retry {retry_times}/{max_retry_times}"
                )
            time.sleep(retry_times * 0.5)
            continue

        if total is not None and len(buffer) < total:
            continue
        too_long = total is not None and len(buffer) > total
        if too_long or not _match_etag(buffer, etag):
            if verbose:
                logger.warning(
                    f"Downloaded object failed verification, retry {retry_times}/{max_retry_times}"
                )
            buffer, etag, total = bytearray(), None, None
            continue
        return bytes(buffer)
    raise Exception(
        f"Download storage object failed after {max_retry_times} retries: "
        f"received {len(buffer)} of {total} bytes"
    )


def _match_etag(content: bytearray, etag: str) -> bool:
    """ETag 不含 "-" 時等於整個物件的 MD5；分段上傳的 ETag 無法以 MD5 驗證"""
    if not etag:
        return True
    etag = etag.strip('"')
    if "-" in etag:
        return True
    return hashlib.md5(content).hexdigest() == etag


async def _loop_run_get(
    executor: concurrent.futures.ThreadPoolExecutor,
    loop: asyncio.AbstractEventLoop,
    session: requests.Session,
    url: str,
    params: Dict[str, Union[str, int, float]],
    timeout: int = 60,
    max_retry_times: int = 10,
    verbose: bool = False,
):
    """
    將同步 request 包成 async
    """
    return await loop.run_in_executor(
        executor,
        request_get,
        session,
        url,
        params,
        timeout,
        max_retry_times,
        verbose,
    )


def async_request_get(
    session: requests.Session,
    url: str,
    params_list: List[Dict[str, Union[str, int, float]]],
    timeout: int = 60,
    max_retry_times: int = 10,
    verbose: bool = False,
    auto_tune: bool = True,
    max_concurrency: int = None,
    batch_size: int = 10,
):
    """
    批量 async request，支援自動根據機器資源調整 max_concurrency / batch_size
    """
    # 自動調整
    if auto_tune:
        cpu_count = os.cpu_count() or 1
        max_concurrency = max_concurrency or max(1, cpu_count * 2)
    else:
        max_concurrency = max_concurrency or 10

    async def runner():
        semaphore = asyncio.Semaphore(max_concurrency)
        loop = asyncio.get_event_loop()
        executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=max_concurrency
        )

        async def _limited_run(params):
            async with semaphore:
                resp = await _loop_run_get(
                    executor,
                    loop,
                    session,
                    url=url,
                    params=params,
                    timeout=timeout,
                    max_retry_times=max_retry_times,
                    verbose=verbose,
                )
                return resp

        results = []
        pbar = tqdm(total=len(params_list))

        # 分 batch 建立 task
        for i in range(0, len(params_list), batch_size):
            batch = params_list[i : i + batch_size]
            tasks = [asyncio.create_task(_limited_run(p)) for p in batch]

            for coro in asyncio.as_completed(tasks):
                try:
                    res = await coro
                    results.append(res)
                except Exception as exc:
                    if verbose:
                        logger.error(f"Task failed: {exc}")
                pbar.update(1)

        pbar.close()
        executor.shutdown()
        return results

    return asyncio.run(runner())
