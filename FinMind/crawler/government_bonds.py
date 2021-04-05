"""
政府債券
G8-俄羅斯、美國、加拿大、英國、法國、德國、義大利及日本
"""
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


class GovernmentBondsCrawler(BaseCrawler):
    @staticmethod
    def create_loop_list():
        def get_data_id_name(url):

            headers = {
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                "Connection": "keep-alive",
                "Host": "www.investing.com",
                "Referer": url,
                "User-Agent": USER_AGENT,
                "X-Requested-With": "XMLHttpRequest",
            }

            res = requests.get(url, verify=True, headers=headers)
            tem_data_id = re.findall('data-id="[0-9]+"', res.text)
            tem_data_id = [di.replace("data-id=", "") for di in tem_data_id]
            page = etree.HTML(res.text)
            _data_id = []
            _data_name = []
            for di in tem_data_id:
                tem = page.xpath("//span[@data-id={}]".format(di))
                if len(tem) > 0:
                    _data_id.append(tem[0].attrib["data-id"])
                    _data_name.append(tem[0].attrib["data-name"])

            return _data_id, _data_name

        def get_country_url():
            index_url = "https://www.investing.com/rates-bonds/"
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

            data_country_id = re.findall('data-country-id="[0-9]+"', res.text)
            data_country_id = [
                dci.replace("data-country-id=", "") for dci in data_country_id
            ]
            page = etree.HTML(res.text)
            tem = []
            for dci in data_country_id:
                tem.append(
                    page.xpath("//option[@data-country-id={}]".format(dci))[0]
                )

            url = [
                "https://www.investing.com" + te.attrib["value"] for te in tem
            ]
            # G8 and china
            select = [
                "canada",
                "china",
                "france",
                "germany",
                "japan",
                "russia",
                "uk",
                "usa",
                "italy",
            ]
            countries_url = []
            for url_index in range(len(url)):
                tem = url[url_index].replace(
                    "https://www.investing.com/rates-bonds/", ""
                )
                tem = tem.replace("-government-bonds", "")
                if tem in select:
                    countries_url.append(url[url_index])
            return countries_url

        # main
        country_url = get_country_url()
        loop_list = []
        for curl in country_url:  # curl = country_url[0]
            print(curl)
            data_id, data_name = get_data_id_name(curl)
            for i in range(len(data_id)):
                loop_list.append([data_id[i], data_name[i]])

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

        return "{}/{}/{}".format(m, d, y)

    def crawler(self, loop):  # loop = ['23681', 'Germany 3 Month']
        def get_value(template):

            date = int(template[0].attrib["data-real-value"])
            date = int(date / 60 / 60 / 24)
            date = str(
                datetime.date(1970, 1, 1) + datetime.timedelta(days=date)
            )
            v = [
                float(template[template_index].text)
                for template_index in range(1, 5)
                if template[template_index].text is not None
            ]
            if len(v) == 0:
                return pd.DataFrame()
            _price, _open, _high, _low = v
            change = (
                float(template[5].text.replace("%", "").replace(",", "")) / 100
            )

            return pd.DataFrame([date, _price, _open, _high, _low, change]).T

        cid, data_name = loop
        header = data_name + " Bond Yield Historical data"
        st_date, end_date = (
            "01/01/1970",
            self.get_end_date(),
        )
        bonds_url = "https://www.investing.com/instruments/HistoricalDataAjax"

        form_data = {
            "curr_id": cid,
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
            "Content-Length": "192",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "www.investing.com",
            "Origin": "https://www.investing.com",
            "Referer": "https://www.investing.com/rates-bonds/france-1-month-bond-yield-historical-data",
            "User-Agent": USER_AGENT,
            "X-Requested-With": "XMLHttpRequest",
        }
        print("requests post")
        res = requests.post(
            bonds_url, verify=True, headers=headers, data=form_data
        )
        print("data clean")
        page = etree.HTML(res.text)
        tr_path = page.xpath("//tr")

        col_name = [col.text for col in tr_path[0].xpath("//th")]
        col_name = [c.replace(" %", "Percent") for c in col_name]
        col_name = ["date" if c == "Date" else c for c in col_name]
        data = pd.DataFrame()
        td_path = page.xpath("//tr//td")
        for i in range(0, len(td_path) - 6, 6):
            tem = td_path[i : i + 6]
            value = get_value(tem)
            if len(value) > 0:
                data = data.append(value)

        if len(data) > 0:
            data.columns = col_name
            data["name"] = "{}".format(data_name)
            # data['data_id'] = cid
            data = data.sort_values("date")
            data.index = range(len(data))

        return data
