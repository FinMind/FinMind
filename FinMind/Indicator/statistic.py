import pandas as pd
import numpy as np
import math

from collections import deque
from sklearn.linear_model import LinearRegression

def standard_deviation(pd_data, period, column_name, mode='sample'):
    """
    Knowledge:
        mode = 1. Sample     樣本的標準差 ddof = 1 pandas
               2. Population 母體的標準差 ddof = 0 talib
    """
    _ddof = 1 if mode=='sample' else 0
    rolling_std = pd_data[column_name].rolling(period).std(ddof=_ddof) # default ddof = 1
    return rolling_std

def linear_regression(pd_src, period, column_name):
    intercept_list = list()
    slope_list     = list()
    queue = deque([])
    model = LinearRegression()

    slope     = np.NaN
    intercept = np.NaN

    X = np.reshape(list(range(0, period)), [period, 1])
    for index, row in pd_src.iterrows():
        if row[column_name] != row[column_name]:
            intercept_list.append(np.NaN)
            slope_list.append(np.NaN)
            continue

        queue.append(row[column_name])
        if len(queue) != period:
            intercept_list.append(np.NaN)
            slope_list.append(np.NaN)
            continue

        Y = np.reshape(queue, [period, 1])

        model.fit(X, Y)
        intercept_list.append(model.intercept_[0])
        slope_list.append(model.coef_[0][0])
        queue.popleft()

    pd_linear_reg_intercept = pd.DataFrame(intercept_list)
    pd_linear_reg_slope     = pd.DataFrame(slope_list)
    return pd_linear_reg_intercept, pd_linear_reg_slope


# Nickname
stddev           = standard_deviation
linreg           = linear_regression
