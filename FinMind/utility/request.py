import asyncio
import concurrent.futures
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
