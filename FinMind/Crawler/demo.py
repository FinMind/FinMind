import pandas as pd
from FinMind.Crawler import RawMaterialFuturesPrices
from FinMind.Crawler import GovernmentBonds

# -------------------------------------------------------------------
RMFP = RawMaterialFuturesPrices.Crawler()
# get futures list
loop_list = RMFP.create_loop_list()

# get one futures data
data = RMFP.crawler(loop_list[0])

# or get all futures data
data = pd.DataFrame()
for loop in loop_list:
    print(loop)
    value = RMFP.crawler(loop)
    data = data.append(value)

# -------------------------------------------------------------------
GB = GovernmentBonds.Crawler()
# get futures list
loop_list = GB.create_loop_list()

# get one futures data
data = GB.crawler(loop_list[0])

# or get all futures data
data = pd.DataFrame()
for loop in loop_list:
    print(loop)
    value = GB.crawler(loop)
    data = data.append(value)
