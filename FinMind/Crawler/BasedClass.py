import datetime
import numpy as np
import requests
import time


def requests_get(url, header):
    try:
        res = requests.get(url, verify=False, timeout=10, headers=header)
        return res
    except Exception as e:
        if "Max retries exceeded" in str(e) or "Read timed out" in str(e):
            time.sleep(60)


def requests_post(url, header, form_data):
    try:
        res = requests.post(
            url, verify=False, timeout=10, headers=header, data=form_data
        )
        return res
    except Exception as e:
        if "Max retries exceeded" in str(e) or "Read timed out" in str(e):
            time.sleep(60)
            raise


def get_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))


class Crawler:
    def date2days(self, date):
        # date = '2018-08-03'
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        value = (date - datetime.date(1970, 1, 1)).days
        value = value * 60 * 60 * 24 * 1000
        return value

    def days2date(self, day):
        # day = 631497600000
        # 60s = 1min
        # 60min = 1hr
        day = int(day)
        day = int(day / 1000 / 60 / 60 / 24)
        value = datetime.date(1970, 1, 1) + datetime.timedelta(days=day)
        return value

    def millisecond2date(self, ms):
        # ms = 1559489350000
        ms = int(ms)
        date = str(self.days2date(ms))
        days = int(ms / 1000 / 60 / 60 / 24)

        second = ms / 1000 - days * 60 * 60 * 24
        hour = int(second / 60 / 60)
        minute = int((second - hour * 60 * 60) / 60) - 1

        if hour < 0:
            hour = "00"
        elif hour < 10:
            hour = "0" + str(hour)
        else:
            hour = str(hour)

        if minute < 0:
            minute = "00"
        elif minute < 10:
            minute = "0" + str(minute)
        else:
            minute = str(minute)
        # second = (second - hour*60*60 - minute*60)#hour
        value = date + " " + hour + ":" + minute + ":00"
        return value

    def millisecond2date2(self, ms):
        # ms = 1566898740000
        ms = int(ms)
        date = str(self.days2date(ms))
        days = int(ms / 1000 / 60 / 60 / 24)

        second = ms / 1000 - days * 60 * 60 * 24
        hour = int(second / 60 / 60)
        minute = int((second - hour * 60 * 60) / 60)
        second = int(second - hour * 60 * 60 - minute * 60)

        if hour < 0:
            hour = "00"
        elif hour < 10:
            hour = "0" + str(hour)
        else:
            hour = str(hour)

        if minute < 0:
            minute = "00"
        elif minute < 10:
            minute = "0" + str(minute)
        else:
            minute = str(minute)
        # second = (second - hour*60*60 - minute*60)#hour
        if second < 10:
            second = "0{}".format(second)
        value = "{} {}:{}:{}".format(date, hour, minute, second)
        return value

    def date2millisecond(self, date):
        # date = '2019-06-02 15:30:00'
        date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        date = date + datetime.timedelta(minutes=1)
        second = date - datetime.datetime(1970, 1, 1, 0, 0, 0)

        second = second.days * 24 * 60 * 60 + second.seconds
        # ms = ms*1000

        return second

    def create_date(self, start, today=False):  # start = '2018-07-31'
        start = datetime.datetime.strptime(
            start, "%Y-%m-%d"
        ).date() + datetime.timedelta(days=1)
        end = datetime.date.today()

        day_len = (end - start).days
        if today:
            day_len = (end - start).days + 1
        date = [
            str(start + datetime.timedelta(days=dat)) for dat in range(day_len)
        ]
        return date

    def remove_outlier(self, data, var_name):

        value = list(data[var_name])
        mean = np.mean(value, axis=0)
        sd = np.std(value, axis=0)
        if sd < 1:
            return data

        _bool = []
        for x in value:
            if (5 * mean) > x > (-5 * mean):
                _bool.append(True)
            else:
                _bool.append(False)

        data = data[_bool]
        return data


def change_chinese_date_us(d):
    y, m, d = [int(x) for x in d.split("/")]
    y = y + 1911
    date = datetime.date(y, m, d)
    return date
