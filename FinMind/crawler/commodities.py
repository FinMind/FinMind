import datetime
import os
import re
import sys

import pandas as pd
import requests
from lxml import etree

from FinMind.crawler.base import BaseCrawler, USER_AGENT

PATH = "/".join(os.path.abspath(__file__).split("/")[:-2])
sys.path.append(PATH)


class CommoditiesCrawler(BaseCrawler):
    def __init__(self):
        super(CommoditiesCrawler, self).__init__()

    @staticmethod
    def create_loop_list():
        # self.based_url = 'https://www.investing.com/commodities/'
        kind_list = ["meats", "grains", "energies", "softs", "metals"]
        loop_list = []
        for kind in kind_list:
            print(kind)
            index_url = "https://www.investing.com/commodities/" + kind
            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive",
                "Host": "www.investing.com",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": USER_AGENT,
            }
            res = requests.get(index_url, verify=True, headers=headers)

            tem = re.findall(
                ' data-name="[A-Za-z ]+" data-id="[0-9]+" ', res.text
            )
            futures_id_list = [re.findall("[0-9]+", te)[0] for te in tem]
            data_name_list = [
                re.findall('"[A-Za-z ]+"', te)[0].replace('"', "") for te in tem
            ]
            [
                loop_list.append([futures_id_list[i], data_name_list[i]])
                for i in range(len(futures_id_list))
            ]
        return loop_list

    @staticmethod
    def get_end_date():
        end_date = datetime.datetime.now().date()
        end_date = end_date + datetime.timedelta(-1)
        y = str(end_date.year)
        m = (
            str(end_date.month)
            if end_date.month > 9
            else "0" + str(end_date.month)
        )
        d = str(end_date.day) if end_date.day > 9 else "0" + str(end_date.day)

        return m + "/" + d + "/" + y

    def crawler(self, loop):  # loop = ['49769', 'Brent Oil Futures']
        def get_value(template):

            date = int(template[0].attrib["data-real-value"])
            date = int(date / 60 / 60 / 24)
            date = str(
                datetime.date(1970, 1, 1) + datetime.timedelta(days=date)
            )
            v = [
                float(
                    template[template_index]
                    .attrib["data-real-value"]
                    .replace(",", "")
                )
                for template_index in range(1, 6)
            ]
            _price, _open, _high, _low, _vol = v

            change = (
                float(template[6].text.replace("%", "").replace(",", "")) / 100
            )

            return pd.DataFrame(
                [date, _price, _open, _high, _low, _vol, change]
            ).T

        # -------------------------------------------------------------------
        futures_id, data_name = loop
        header = data_name + " Historical data"
        st_date, end_date = (
            "01/01/1970",
            self.get_end_date(),
        )

        bonds_url = "https://www.investing.com/instruments/HistoricalDataAjax"
        form_data = {
            "curr_id": futures_id,
            "header": header,
            "st_date": st_date,
            "end_date": end_date,
            "interval_sec": "Daily",
            "sort_col": "date",
            "sort_ord": "DESC",
            "action": "historical_data",
        }

        headers = {
            "Accept": "text/plain, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Content-Length": "183",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "www.investing.com",
            "Origin": "https://www.investing.com",
            "Referer": "https://www.investing.com/commodities/brent-oil-historical-data",
            "User-Agent": USER_AGENT,
            "X-Requested-With": "XMLHttpRequest",
        }
        print("requests post")
        res = requests.post(
            bonds_url, verify=True, headers=headers, data=form_data
        )
        print("data clean")
        page = etree.HTML(res.text)
        col_name = page.xpath("//tr//th")

        col_name = [
            c.text.replace(" %", "Percent").replace(".", "") for c in col_name
        ]
        col_name = ["date" if c == "Date" else c for c in col_name]

        data = pd.DataFrame()
        td_path = page.xpath("//tr//td")
        for i in range(0, len(td_path) - 7, 7):
            tem = td_path[i : i + 7]
            value = get_value(tem)
            data = data.append(value)

        if len(data) > 0:
            data.columns = col_name
            data["name"] = data_name
            # data['data_id'] = futures_id
            data = data.sort_values("date")
            data.index = range(len(data))

        return data
