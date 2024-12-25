import ssl
import time
from typing import Dict, List, Union

import requests
import urllib3
from loguru import logger
from tqdm import tqdm

try:
    import asyncio
    import concurrent.futures

    import nest_asyncio

    nest_asyncio.apply()  # for Jupyter Notebook
except Exception as error_msg:
    logger.warning(f"import error: {error_msg}")


def request_get(
    url: str,
    params: Dict[str, Union[int, str, float]],
    timeout: int = 30,
    max_retry_times: int = 10,
):
    for retry_times in range(max_retry_times):
        try:
            response = requests.get(
                url, verify=True, params=params, timeout=timeout
            )
            if response.status_code == 504:
                logger.warning(
                    f"status_code = 504, retry {retry_times} and sleep {retry_times * 0.1} seonds"
                )
                time.sleep(retry_times * 0.1)
            else:
                break
        except requests.Timeout as exc:
            raise Exception(f"Timeout {timeout} seconds")
        except (
            requests.ConnectionError,
            ssl.SSLError,
            urllib3.exceptions.ReadTimeoutError,
            urllib3.exceptions.ProtocolError,
        ) as exc:
            logger.warning(
                f"{exc}, retry {retry_times} and sleep {retry_times * 0.1} seonds"
            )
            time.sleep(retry_times * 0.1)
        except Exception as exc:
            raise Exception(exc)

    if response.status_code == 200:
        pass
    else:
        logger.error(params)
        raise Exception(response.text)
    return response


async def _loop_run_get(
    executor: concurrent.futures.ThreadPoolExecutor,
    loop: asyncio,
    url: str,
    params: Dict[str, Union[str, int, float]],
    timeout: int = 30,
):
    resp = await loop.run_in_executor(
        executor, request_get, url, params, timeout
    )
    return resp


def async_request_get(
    url: str,
    params_list: List[Dict[str, Union[str, int, float]]] = None,
    timeout: int = 30,
):
    async def async_batch_get(executor, params_list, timeout):
        loop = asyncio.get_event_loop()
        task_list = [
            loop.create_task(
                _loop_run_get(
                    executor,
                    loop,
                    url=url,
                    params=params_list[i],
                    timeout=timeout,
                )
            )
            for i in tqdm(range(len(params_list)))
        ]
        resp_list = await asyncio.gather(*task_list)
        return resp_list

    # async
    executor = concurrent.futures.ThreadPoolExecutor()
    resp_list = asyncio.run(
        async_batch_get(executor, params_list=params_list, timeout=timeout)
    )
    executor.shutdown()
    return resp_list
