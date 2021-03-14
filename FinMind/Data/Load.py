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


def get_retroactive_price(
        stock_id: str = "",
        start_date: str = "",
        end_date: str = "",
        user_id: str = "",
        password: str = "",
) -> pd.DataFrame:
    """
    取得還原股價
    """
    stock_price = FinData(dataset="TaiwanStockPrice", select=stock_id, date=start_date, end_date=end_date,
                          user_id=user_id, password=password)
    ex_dividend_api = f"https://api.finmindtrade.com/api/v4/data"
    params = {
        "dataset": "TaiwanStockDividendResult",
        "data_id": stock_id,
        "start_date": start_date,
        "end_date": end_date,
    }
    ex_dividend_data = requests.get(ex_dividend_api, params=params)
    ex_dividend_price = pd.DataFrame(ex_dividend_data.json()['data'])
    if len(ex_dividend_price) == 0:
        return stock_price
    ex_dividend_price = ex_dividend_price[['date', 'stock_and_cache_dividend']]
    stock_price['date'] = pd.to_datetime(stock_price['date'])
    ex_dividend_price['date'] = pd.to_datetime(ex_dividend_price['date'])
    stock_price['change'] = stock_price['close'].pct_change(periods=1)
    ex_dividend_price = ex_dividend_price.iloc[::-1].reset_index(drop=True)
    stock_price = stock_price.iloc[::-1].reset_index(drop=True)
    stock_price['retroactive_open'] = stock_price['open']
    stock_price['retroactive_max'] = stock_price['max']
    stock_price['retroactive_min'] = stock_price['min']
    stock_price['retroactive_close'] = stock_price['close']
    stock_price['retroactive_change'] = stock_price['change']
    for index, data in ex_dividend_price.iterrows():
        ex_dividend_date = data['date']
        ex_dividend_date_y1 = stock_price[stock_price['date'] <= ex_dividend_date].iloc[1][0]
        calibration_price = stock_price[stock_price['date'] == ex_dividend_date_y1]['retroactive_close'].iloc[0] - data[
            'stock_and_cache_dividend']
        stock_price.loc[stock_price['date'] == ex_dividend_date_y1, ['retroactive_close']] = calibration_price
        calibration_change = (stock_price[stock_price['date'] == ex_dividend_date]['retroactive_close'].iloc[
                                  0] - calibration_price) / calibration_price
        stock_price.loc[stock_price['date'] == ex_dividend_date, ['retroactive_change']] = calibration_change
    for i in range(len(stock_price)):
        stock_price.loc[i + 1, 'retroactive_close'] = (
                stock_price.loc[i, 'retroactive_close'] / (1 + stock_price.loc[i, 'retroactive_change']))
        stock_price.loc[i, 'retroactive_open'] = (stock_price.loc[i, 'retroactive_close'] * (
                1 + (stock_price.loc[i, 'open'] - stock_price.loc[i, 'close']) / stock_price.loc[i, 'close']))
        stock_price.loc[i, 'retroactive_max'] = (stock_price.loc[i, 'retroactive_close'] * (
                1 + (stock_price.loc[i, 'max'] - stock_price.loc[i, 'close']) / stock_price.loc[i, 'close']))
        stock_price.loc[i, 'retroactive_min'] = (stock_price.loc[i, 'retroactive_close'] * (
                1 + (stock_price.loc[i, 'min'] - stock_price.loc[i, 'close']) / stock_price.loc[i, 'close']))
    stock_price['open'] = stock_price['retroactive_open'].round(2)
    del stock_price['retroactive_open']
    stock_price['max'] = stock_price['retroactive_max'].round(2)
    del stock_price['retroactive_max']
    stock_price['min'] = stock_price['retroactive_min'].round(2)
    del stock_price['retroactive_min']
    stock_price['close'] = stock_price['retroactive_close'].round(2)
    del stock_price['retroactive_close']
    del stock_price['change']
    del stock_price['retroactive_change']
    stock_price['spread'] = stock_price['close'] - stock_price['close'].shift(1)
    stock_price = stock_price.dropna()
    stock_price = stock_price.iloc[::-1].reset_index(drop=True)
    return stock_price
