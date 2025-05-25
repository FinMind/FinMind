import ssl
import sys
import time
import typing

import pandas as pd
import requests
import urllib3
from loguru import logger

from FinMind.schema.data import Dataset
from FinMind.utility.request import async_request_get, request_get

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
    def api_usage(
        self,
        timeout: int = 5,
    ) -> int:
        headers = {"Authorization": f"Bearer {self.__api_token}"}
        url = "https://api.web.finmindtrade.com/v2/user_info"
        response = request_get(
            url,
            headers=headers,
            timeout=timeout,
        ).json()
        return response.get("user_count", 0)

    @property
    def api_usage_limit(
        self,
        timeout: int = 5,
    ) -> int:
        headers = {"Authorization": f"Bearer {self.__api_token}"}
        url = "https://api.web.finmindtrade.com/v2/user_info"
        logger.debug(headers)
        response = request_get(
            url,
            headers=headers,
            timeout=timeout,
        ).json()
        return response.get("api_request_limit", 0)

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

    def _compatible_endpoints_param(self, params: str) -> dict:
        if params["dataset"] in (
            "TaiwanStockTradingDailyReport",
            "TaiwanStockWarrantTradingDailyReport",
        ):
            if "start_date" in params:
                params["date"] = params.pop("start_date")
        return params

    def _dispatcher_url(self, dataset: str) -> str:
        base_url = f"{self.__api_url}/{self.__api_version}"
        url_mapping = {
            "TaiwanStockTradingDailyReportSecIdAgg": f"{base_url}/taiwan_stock_trading_daily_report_secid_agg",
            "TaiwanStockTradingDailyReport": f"{base_url}/taiwan_stock_trading_daily_report",
            "TaiwanStockWarrantTradingDailyReport": f"{base_url}/taiwan_stock_warrant_trading_daily_report",
        }
        return url_mapping.get(dataset, f"{base_url}/data")

    def get_data(
        self,
        dataset: Dataset,
        data_id: str = "",
        securities_trader_id: str = "",
        stock_id: str = "",
        start_date: str = "",
        data_id_list: typing.List[str] = None,
        # securities_trader_id_list: typing.List[str] = None,
        end_date: str = "",
        timeout: int = None,
        use_async: bool = False,
    ) -> pd.DataFrame:
        """
        :param params: finmind api參數
        :return:
        """
        if use_async:
            return self._get_data_with_async(
                dataset=dataset,
                data_id_list=data_id_list,
                # securities_trader_id_list=securities_trader_id_list,
                start_date=start_date,
                end_date=end_date,
            )
        else:
            logger.info(f"download {dataset}, data_id: {data_id}")
            params = dict(
                dataset=dataset,
                data_id=data_id,
                securities_trader_id=securities_trader_id,
                stock_id=stock_id,
                start_date=start_date,
                end_date=end_date,
                user_id=self.__user_id,
                password=self.__password,
                device=self.__device,
            )
            params = self._compatible_api_version(params)
            params = self._compatible_endpoints_param(params)
            headers = {"Authorization": f"Bearer {self.__api_token}"}
            url = self._dispatcher_url(dataset)
            logger.debug(params)
            response = request_get(
                url,
                params=params,
                headers=headers,
                timeout=timeout,
            ).json()
            return pd.DataFrame(response["data"])

    def _get_data_with_async(
        self,
        dataset: Dataset,
        data_id_list: typing.List[str] = None,
        # securities_trader_id_list: typing.List[str] = None,
        start_date: str = "",
        end_date: str = "",
        timeout: int = None,
    ) -> pd.DataFrame:
        """
        :param params: finmind api參數
        :return:
        """
        logger.info(f"download {dataset}, data_id: {data_id_list}")
        params_list = [
            self._compatible_endpoints_param(
                self._compatible_api_version(
                    params=dict(
                        dataset=dataset,
                        data_id=data_id,
                        start_date=start_date,
                        end_date=end_date,
                        user_id=self.__user_id,
                        password=self.__password,
                        device=self.__device,
                    )
                )
            )
            for data_id in data_id_list
        ]
        headers = {"Authorization": f"Bearer {self.__api_token}"}
        url = self._dispatcher_url(dataset)
        resp_list = async_request_get(
            url,
            params_list=params_list,
            headers=headers,
            timeout=timeout,
        )
        data_list = []
        [data_list.extend(resp.json()["data"]) for resp in resp_list]
        df = pd.DataFrame(data_list)
        return df

    def get_taiwan_stock_tick_snapshot(
        self,
        dataset: Dataset,
        data_id: typing.Union[str, typing.List[str]] = "",
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
            device=self.__device,
        )
        headers = {"Authorization": f"Bearer {self.__api_token}"}
        params = self._compatible_api_version(params)
        url = (
            f"{self.__api_url}/{self.__api_version}/taiwan_stock_tick_snapshot"
        )
        logger.debug(params)
        response = request_get(
            url,
            params=params,
            headers=headers,
            timeout=timeout,
        ).json()
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
            device=self.__device,
        )
        headers = {"Authorization": f"Bearer {self.__api_token}"}
        params = self._compatible_api_version(params)
        url = f"{self.__api_url}/{self.__api_version}/taiwan_futures_snapshot"
        logger.debug(params)
        response = request_get(
            url,
            params=params,
            headers=headers,
            timeout=timeout,
        ).json()
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
            device=self.__device,
        )
        headers = {"Authorization": f"Bearer {self.__api_token}"}
        params = self._compatible_api_version(params)
        url = f"{self.__api_url}/{self.__api_version}/taiwan_options_snapshot"
        logger.debug(params)
        response = request_get(
            url,
            params=params,
            headers=headers,
            timeout=timeout,
        ).json()
        return pd.DataFrame(response["data"])

    def get_datalist(self, dataset: str, timeout: int = None) -> pd.DataFrame:
        # 測試不支援以token方式獲取
        if not self.__user_id:
            raise Exception("please login by account")
        params = {
            "dataset": dataset,
            "device": self.__device,
        }
        headers = {"Authorization": f"Bearer {self.__api_token}"}
        url = f"{self.__api_url}/{self.__api_version}/datalist"
        data = request_get(
            url,
            params=params,
            headers=headers,
            timeout=timeout,
        ).json()
        data = data["data"]
        return data

    def translation(self, dataset: str, timeout: int = None) -> pd.DataFrame:
        # 測試v4不支援
        params = {
            "dataset": dataset,
            "device": self.__device,
        }
        headers = {"Authorization": f"Bearer {self.__api_token}"}
        url = f"{self.__api_url}/{self.__api_version}/translation"
        data = request_get(
            url,
            params=params,
            headers=headers,
            timeout=timeout,
        ).json()
        data = pd.DataFrame(data["data"])
        return data
