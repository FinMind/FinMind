import sys

import pandas as pd
import requests
from loguru import logger

logger.remove()
logger.add(sys.stderr, level="INFO")


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
        login_info = requests.post(url, data=payload).json()
        logger.debug(login_info)
        if login_info.get("status", 0) == 200:
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
        else:
            if "date" in params:
                params["start_date"] = params.pop("date")
            if "stock_id" in params:
                params["data_id"] = params.pop("stock_id")
        return params

    def get_data(self, **params) -> pd.DataFrame:
        """
        :param params: finmind api參數
        :return:
        """
        params.update(
            dict(
                user_id=self.__user_id,
                password=self.__password,
                token=self.__api_token,
                device=self.__device,
            )
        )
        params = self._compatible_api_version(params)
        url = f"{self.__api_url}/{self.__api_version}/data"
        logger.debug(params)
        response = requests.get(url, verify=True, params=params).json()
        if "msg" not in response or response["msg"] != "success":
            logger.error(params)
            raise Exception(response)
        return pd.DataFrame(response["data"])

    def get_datalist(self, dataset: str) -> pd.DataFrame:
        # 測試不支援以token方式獲取
        if not self.__user_id:
            raise Exception("please login by account")
        params = {
            "dataset": dataset,
            "token": self.__api_token,
            "device": self.__device,
        }
        url = f"{self.__api_url}/{self.__api_version}/datalist"
        res = requests.get(url, verify=True, params=params)
        data = res.json()
        if data.get("status", 200) == 200:
            data = data["data"]
        return data

    def translation(self, dataset: str) -> pd.DataFrame:
        # 測試v4不支援
        params = {
            "dataset": dataset,
            "token": self.__api_token,
            "device": self.__device,
        }
        url = f"{self.__api_url}/{self.__api_version}/translation"
        res = requests.get(url, verify=True, params=params)
        data = res.json()
        if data.get("status", 0) == 200:
            data = pd.DataFrame(data["data"])
        return data
