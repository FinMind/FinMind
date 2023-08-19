import ssl
import sys
import time
import typing

import pandas as pd
import requests
import urllib3
from loguru import logger

from FinMind.schema.data import Dataset

logger.remove()
logger.add(sys.stderr, level="INFO")


def request_get(
    url: str,
    params: typing.Dict[str, typing.Union[int, str, float]],
    timeout: int = None,
):
    for i in range(10):
        try:
            response = requests.get(
                url, verify=True, params=params, timeout=timeout
            )
            break
        except requests.Timeout as exc:
            raise Exception("Timeout")
        except (
            requests.ConnectionError,
            ssl.SSLError,
            urllib3.exceptions.ReadTimeoutError,
            urllib3.exceptions.ProtocolError,
        ) as exc:
            logger.warning(f"{exc}, retry {i} and sleep {i * 0.1} seonds")
            time.sleep(i * 0.1)
    if response.json()["msg"] == "success" and response.status_code == 200:
        pass
    else:
        logger.error(params)
        raise Exception(response.text)
    return response


class FinMindApi:
    def __init__(self):
        self.__user_id = ""
        self.__password = ""
        self.__api_token = ""
        self.__api_url = "https://api.finmindtrade.com/api"
        self.__api_version = "v4"
        self.__device = "package"
        self.__valid_versions = ["v3", "v4"]

    @property
    def api_version(self):
        return self.__api_version

    @api_version.setter
    def api_version(self, version: str):
        if version not in self.__valid_versions:
            logger.error(
                f"Invalid version name:{version}, The supported version is set to{' '.join(self.__valid_versions)}"
            )
            return
        self.__api_version = version

    def login(self, user_id: str, password: str):
        """
        :param user_id: finmind 使用者賬號
        :param password: finmind 使用者密碼
        :return: True if success login.
        """
        payload = {
            "user_id": user_id,
            "password": password,
            "device": self.__device,
        }
        url = f"{self.__api_url}/{self.__api_version}/login"
        resp = requests.post(url, data=payload)
        login_info = resp.json()
        logger.debug(login_info)
        if resp.status_code == 200:
            self.__api_token = login_info.get("token", "")
            self.__user_id = user_id
            self.__password = password
            logger.info("Login success")
            return True
        else:
            raise Exception(login_info["msg"])

    def login_by_token(self, api_token: str):
        """
        :param api_token: finmind api token
        """
        self.__api_token = api_token

    def _compatible_api_version(self, params):
        if self.__api_version == "v3":
            if "start_date" in params:
                params["date"] = params.pop("start_date")
            if "data_id" in params:
                params["stock_id"] = params.pop("data_id")
        elif self.__api_version == "v4":
            if "date" in params:
                params["start_date"] = params.pop("date")
        return params

    def get_data(
        self,
        dataset: Dataset,
        data_id: str = "",
        stock_id: str = "",
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
    ) -> pd.DataFrame:
        """
        :param params: finmind api參數
        :return:
        """
        params = dict(
            dataset=dataset,
            data_id=data_id,
            stock_id=stock_id,
            start_date=start_date,
            end_date=end_date,
            user_id=self.__user_id,
            password=self.__password,
            token=self.__api_token,
            device=self.__device,
        )
        params = self._compatible_api_version(params)
        url = f"{self.__api_url}/{self.__api_version}/data"
        logger.debug(params)
        response = request_get(url, params, timeout).json()
        return pd.DataFrame(response["data"])

    def get_taiwan_stock_tick_snapshot(
        self,
        dataset: Dataset,
        data_id: str = "",
        timeout: int = None,
    ) -> pd.DataFrame:
        """
        :param params: finmind api參數
        :return:
        """
        params = dict(
            dataset=dataset,
            data_id=data_id,
            user_id=self.__user_id,
            password=self.__password,
            token=self.__api_token,
            device=self.__device,
        )
        params = self._compatible_api_version(params)
        url = (
            f"{self.__api_url}/{self.__api_version}/taiwan_stock_tick_snapshot"
        )
        logger.debug(params)
        response = request_get(url, params, timeout).json()
        return pd.DataFrame(response["data"])

    def get_taiwan_futures_snapshot(
        self,
        dataset: Dataset,
        data_id: str = "",
        timeout: int = None,
    ) -> pd.DataFrame:
        """
        :param params: finmind api參數
        :return:
        """
        params = dict(
            dataset=dataset,
            data_id=data_id,
            user_id=self.__user_id,
            password=self.__password,
            token=self.__api_token,
            device=self.__device,
        )
        params = self._compatible_api_version(params)
        url = f"{self.__api_url}/{self.__api_version}/taiwan_futures_snapshot"
        logger.debug(params)
        response = request_get(url, params, timeout).json()
        return pd.DataFrame(response["data"])

    def get_taiwan_options_snapshot(
        self,
        dataset: Dataset,
        data_id: str = "",
        timeout: int = None,
    ) -> pd.DataFrame:
        """
        :param params: finmind api參數
        :return:
        """
        params = dict(
            dataset=dataset,
            data_id=data_id,
            user_id=self.__user_id,
            password=self.__password,
            token=self.__api_token,
            device=self.__device,
        )
        params = self._compatible_api_version(params)
        url = f"{self.__api_url}/{self.__api_version}/taiwan_options_snapshot"
        logger.debug(params)
        response = request_get(url, params, timeout).json()
        return pd.DataFrame(response["data"])

    def get_datalist(self, dataset: str, timeout: int = None) -> pd.DataFrame:
        # 測試不支援以token方式獲取
        if not self.__user_id:
            raise Exception("please login by account")
        params = {
            "dataset": dataset,
            "token": self.__api_token,
            "device": self.__device,
        }
        url = f"{self.__api_url}/{self.__api_version}/datalist"
        data = request_get(url, params, timeout).json()
        data = data["data"]
        return data

    def translation(self, dataset: str, timeout: int = None) -> pd.DataFrame:
        # 測試v4不支援
        params = {
            "dataset": dataset,
            "token": self.__api_token,
            "device": self.__device,
        }
        url = f"{self.__api_url}/{self.__api_version}/translation"
        data = request_get(url, params, timeout).json()
        data = pd.DataFrame(data["data"])
        return data
