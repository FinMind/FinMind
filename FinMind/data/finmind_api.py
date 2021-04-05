import pandas as pd
import requests
from loguru import logger


class FinMindApi:
    def __init__(self):
        self.__user_id = ""
        self.__password = ""
        self.__api_token = ""
        self.__api_url = "https://api.finmindtrade.com/api"
        self.__api_version = "v4"
        self.__device = "package"

    @property
    def api_version(self):
        return self.__api_version

    def set_api_version(self, version: str):
        self.__api_version = version

    def login(self, user_id: str, password: str):
        """
        @param user_id: finmind 使用者賬號
        @param password: finmind 使用者密碼
        @return:
        """
        payload = {
            "user_id": user_id,
            "password": password,
            "device": self.__device,
        }
        url = f"{self.__api_url}/{self.__api_version}/login"
        login_info = requests.post(url, data=payload).json()
        if login_info.get("status", 0) == 200:
            logger.info(login_info)
            self.__api_token = login_info.get("token", "")
            self.__user_id = user_id
            self.__password = password
            logger.info("Login success")
            return True
        else:
            raise Exception(login_info["msg"])

    def login_by_token(self, api_token: str):
        """
        @param api_token: finmind api token
        @return:
        """
        self.__api_token = api_token

    def get_data(self, **params) -> pd.DataFrame:
        """
        @param params: finmind api參數
        @return:
        """
        params.update(
            dict(
                user_id=self.__user_id,
                password=self.__password,
                token=self.__api_token,
                device=self.__device,
            )
        )
        url = f"{self.__api_url}/{self.__api_version}/data"
        logger.info(params)
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
        self.url = f"{self.__api_url}/{self.__api_version}/datalist"
        # logger.info(params)
        res = requests.get(self.url, verify=True, params=params)
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
        # logger.info(params)
        res = requests.get(url, verify=True, params=params)
        data = res.json()
        if data.get("status", 0) == 200:
            data = pd.DataFrame(data["data"])
        return data
