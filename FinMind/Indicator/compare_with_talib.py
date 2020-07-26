
from timeit import default_timer as timer
# from ..indicator 
from FinMind.Data import Load
import moving_average as ima
import pandas as pd
import talib
import math

# def COMPARE_SWITCH(Enum):
COMPARE_SWITCH_SMA      = True      # Done
COMPARE_SWITCH_EMA      = True      # Done


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


def simple_download_from_FinMind(code=2330, from_date='2019-1-1'):
    FMDBN = 'TaiwanStockPrice'
    data = Load.FinData(dataset = FMDBN, select = str(code), date = from_date)
    # data.rename({ 'date'             : 'Date', 
    #               'Trading_Volume'   : 'Capacity',
    #               'Trading_money'    : 'Turnover',
    #               'open'             : 'Open',
    #               'max'              : 'High',
    #               'min'              : 'Low',
    #               'close'            : 'Close',
    #               'spread'           : 'Change',
    #               'Trading_turnover' : 'Transaction' }, axis=1, inplace=True)
    return data


def compare_all():
    # ----------------------------------------------------------
    #  Download data
    # ----------------------------------------------------------
    pd_src = simple_download_from_FinMind()

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


compare_all()

