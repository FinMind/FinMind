
from timeit import default_timer as timer
# from ..indicator 
from FinMind.Data import Load
import moving_average as ima
import statistic as iStatistic
import bands as iBands
import pandas as pd
import talib
import math
import requests


# def COMPARE_SWITCH(Enum):
COMPARE_SWITCH_STDDEV   = True      # Done
COMPARE_SWITCH_LINREG   = True      # Done
COMPARE_SWITCH_SMA      = True      # Done
COMPARE_SWITCH_EMA      = False      # Done
COMPARE_SWITCH_BBANDS   = True      # Done

def indicator_compare(pd_personal, pd_talib, message, dates=[]):
    is_same = True
    pd_compare = pd.concat([pd_personal, pd_talib], axis=1)
    pd_compare.columns = ['My', 'TaLib']

    for index, row in pd_compare.iterrows():
        if (math.isnan(row['My']) != math.isnan(row['TaLib']) or abs(row['My']-row['TaLib']) > 0.0000001):
            is_same = False
            if len(dates) > index:
                print('[%d] %s My: %f, TaLib: %f' % (index, dates[index], row['My'], row['TaLib']))
            else:    
                print('[%d] My: %f, TaLib: %f' % (index, row['My'], row['TaLib']))

    if (is_same and len(pd_personal) == len(pd_talib)):
        print(message, 'Same')
    else:
        print(message, 'Inconsistent')


def simple_download_from_FinMind(from_date='2019-01-01'):
    '''
    Return:
        column name : date future_id contract_date     open      max      min    close  spread  spread_per  volume  settlement_price  open_interest trading_session
    '''
    url = "https://api.finmindtrade.com/api/v3/data"
    parameter = {
        "dataset": "TaiwanFuturesDaily",
        "stock_id": "TX",
        "date": from_date,
        "end_date": "2020-04-25",
    }
    resp = requests.get(url, params=parameter)
    data = resp.json()
    pd_data = pd.DataFrame(data['data'])
    pd_data = pd_data.groupby('date', as_index=False).apply(lambda t: t[t.volume==t.volume.max()])
    pd_data.reset_index(drop=True, inplace=True)

    return pd_data

def compare_all():
    # ----------------------------------------------------------
    #  Download data
    # ----------------------------------------------------------
    pd_src = simple_download_from_FinMind()

    # ----------------------------------------------------------
    #  Compare Standard Deviation
    # ----------------------------------------------------------
    if COMPARE_SWITCH_STDDEV:
        period = 20
        close_name = 'close'

        start = timer()
        pd_personal = iStatistic.standard_deviation(pd_src, period, close_name, 'population')
        end = timer()
        print('My    StdDev',end - start)
        
        start = timer()
        pd_talib = talib.STDDEV(pd_src[close_name], period, 1)
        end = timer()
        print('TaLib StdDev',end - start)

        indicator_compare(pd_personal, pd_talib, 'Standard Deviation:')

    # ----------------------------------------------------------
    #  Compare Linear Regression
    # ----------------------------------------------------------
    if COMPARE_SWITCH_LINREG:
        period = 20
        close_name = 'close'

        start = timer()
        pd_linreg_intercept, pd_linreg_slope = iStatistic.linear_regression(pd_src, period, close_name)
        end = timer()
        print('My    LinReg',end - start)

        start = timer()
        pd_talib_intercept  = talib.LINEARREG_INTERCEPT(pd_src[close_name], period)
        pd_talib_slope      = talib.LINEARREG_SLOPE(pd_src[close_name], period)
        end = timer()
        print('TaLib LinReg',end - start)

        indicator_compare(pd_linreg_intercept, pd_talib_intercept, 'Linear Regression Intercept:')
        indicator_compare(pd_linreg_slope, pd_talib_slope, 'Linear Regression Slope:')

    # ----------------------------------------------------------
    #  Compare Simple Moving Average
    # ----------------------------------------------------------
    if COMPARE_SWITCH_SMA:
        period = 20
        close_name = 'close'
        my_indicator_name = '%dMA_%s' % (period, close_name)

        start = timer()
        pd_personal = ima.simple_moving_average(pd_src[close_name], period)
        end = timer()
        print('My    SMA',end - start)
        
        start = timer()
        pd_talib = talib.SMA(pd_src[close_name], period)
        end = timer()
        print('TaLib SMA',end - start)

        indicator_compare(pd_personal, pd_talib, 'Simple Moving Average:')

    # ----------------------------------------------------------
    #  Compare Exponential Moving Average
    # 
    #  >> Personal EMA is not equal to TaLib's, due to TaLib
    #  less than period use sma to get init value.
    # ----------------------------------------------------------
    if COMPARE_SWITCH_EMA:
        period = 10
        close_name = 'close'

        start = timer()
        pd_personal = ima.ema(pd_src[close_name], period)
        end = timer()
        print('My    EMA',end - start)

        start = timer()
        pd_talib = talib.EMA(pd_src[close_name], period)
        end = timer()
        print('TaLib EMA',end - start)

        indicator_compare(pd_personal, pd_talib, 'Exponential Moving Average:')

    if COMPARE_SWITCH_BBANDS:
        period = 20
        period_2 = 2
        close_name = 'close'

        start = timer()
        upperband, middleband, lowerband = iBands.bollinger_bands(pd_src, close_name, period, period_2, 'population')
        end = timer()
        print('My    BBands',end - start)

        start = timer()
        # MA_Type: 0=SMA, 1=EMA, 2=WMA, 3=DEMA, 4=TEMA, 5=TRIMA, 6=KAMA, 7=MAMA, 8=T3 (Default=SMA)
        ta_upperband, ta_middleband, ta_lowerband = talib.BBANDS(pd_src[close_name], period, period_2, period_2, matype=0)
        end = timer()
        print('TaLib BBands',end - start)

        indicator_compare(ta_upperband,  upperband,  'Bollinger Bands Upperband:')
        indicator_compare(ta_middleband, middleband, 'Bollinger Bands Middleband:')
        indicator_compare(ta_lowerband,  lowerband,  'Bollinger Bands Lowerband:')



compare_all()

