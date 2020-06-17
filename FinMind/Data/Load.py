import typing

import numpy as np
import pandas as pd
import requests

from FinMind.config import API_HOST


def FinData(
    dataset: str,
    select: str = "",
    date: str = "",
    end_date: str = "",
    user_id: str = "",
    password: str = "",
    url: str = f"{API_HOST}/data",
) -> pd.DataFrame:

    params = {
        "dataset": dataset,
        "stock_id": select,
        "date": date,
        "end_date": end_date,
        "user_id": user_id,
        "password": password,
    }
    res = requests.get(url, verify=True, params=params)

    data = pd.DataFrame()
    try:
        data = res.json()
        if data["status"] == 200:
            data = pd.DataFrame(data["data"])
    except Exception:
        pass

    return data


def FinDataList(
    dataset: str,
    user_id: str = "",
    password: str = "",
    list_url=f"{API_HOST}/datalist",
) -> typing.List:

    params = {
        "dataset": dataset,
        "user_id": user_id,
        "password": password,
    }
    res = requests.get(list_url, verify=True, params=params)

    data = res.json()
    if data["status"] == 200:
        data = data["data"]

    return data


def CrawlerStockInfo(dataset: str = "") -> pd.DataFrame:
    data = FinData(dataset)
    return data


def transpose(data, var="type"):
    select_variable = "stock_id"
    date_list = list(np.unique(data["date"]))
    data1 = pd.DataFrame()
    select_var_list = list(np.unique(data[select_variable]))
    for date in date_list:
        for select_var in select_var_list:
            data2 = data.loc[
                (data["date"] == date) & (data[select_variable] == select_var),
                [var, "value"],
            ]
            data2.index = data2[var]
            del data2[var]
            data2 = data2.T
            data2.index = range(len(data2))
            data2.columns = list(data2.columns)
            data2["stock_id"] = select_var
            data2["date"] = date
            data1 = data1.append(data2)

    data1.index = range(len(data1))
    return data1


def translation(
    dataset: str, user_id: str = "", password: str = ""
) -> pd.DataFrame:
    url = f"{API_HOST}/translation"
    params = {
        "dataset": dataset,
        "user_id": user_id,
        "password": password,
    }
    res = requests.get(url, verify=True, params=params)
    data = res.json()
    if data["status"] == 200:
        data = pd.DataFrame(data["data"])
    return data
