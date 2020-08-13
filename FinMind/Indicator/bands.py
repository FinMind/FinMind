
import pandas as pd
import numpy as np
import math
import talib

import statistic as istatistic

def bollinger_bands(pd_data, column_name, period=20, K=2, stddev_mode='sample'):
    pd_sma = talib.SMA(pd_data[column_name], period)
    rolling_std = istatistic.standard_deviation(pd_data, period, column_name, stddev_mode) # talib mode
    pd_upper = pd_sma + K*rolling_std
    pd_lower = pd_sma - K*rolling_std
    return pd_upper, pd_sma, pd_lower


# Nickname
bbands = bollinger_bands

