import pandas as pd
import requests


class FinMindApi:
    def __init__(self):
        self.user_id = ""
        self.password = ""
        self._api_token = ""
        self._api_version = "v3"
        self.api_url = {
            "v3": "https://api.finmindtrade.com/api/v3",
            "v4": "https://api.finmindtrade.com/api/v4"
        }

    @property
    def api_version(self):
        return self._api_version

    @api_version.setter
    def api_version(self, version):
        if version not in ["v3", "v4"]:
            raise Exception("Not support version:" + version)
        self._api_version = version

    def login_by_account(self, user_id: str, password: str):
        """
        @param user_id: finmind 使用者賬號
        @param password: finmind 使用者密碼
        @return:
        """
        if not user_id or not password:
            print("Login Fail: account invalid")
            return
        url = self.api_url[self._api_version] + "/login"
        payload = {
            "user_id": user_id,
            "password": password,
        }
        login_info = requests.post(url, data=payload).json()
        if login_info['msg'] == "success":
            self._api_token = login_info['token']
            self.user_id = user_id
            self.password = password
            print("Login success")
        else:
            raise Exception(login_info['msg'])

    def login_by_token(self, api_token: str):
        """
        @param api_token: finmind api token
        @return:
        """
        self._api_token = api_token

    def get_data(self, **params) -> pd.DataFrame:
        """
        @param params: finmind api參數
        @return:
        """
        url = self.api_url[self._api_version] + "/data"
        if self._api_version == "v3" and self.user_id:
            params['user_id'] = self.user_id
            params['password'] = self.password
        elif self._api_token:
            params['token'] = self._api_token
        response = requests.get(url, verify=True, params=params).json()
        if "msg" not in response or response['msg'] != "success":
            raise Exception(response)
        return pd.DataFrame(response["data"])

    def get_datalist(self, dataset):
        # 測試不支援以token方式獲取
        if not self.user_id:
            raise Exception("please login by account")
        url = self.api_url[self._api_version] + "/datalist"
        params = {
            "dataset": dataset,
            "user_id": self.user_id,
            "password": self.password,
        }
        res = requests.get(url, verify=True, params=params)
        data = res.json()
        if data["status"] == 200:
            data = data["data"]
        return data

    def translation(self, dataset: str) -> pd.DataFrame:
        # 測試v4不支援
        url = self.api_url["v3"] + "/translation"
        params = {
            "dataset": dataset,
            "user_id": self.user_id,
            "password": self.password,
        }
        res = requests.get(url, verify=True, params=params)
        data = res.json()
        if data["status"] == 200:
            data = pd.DataFrame(data["data"])
        return data
