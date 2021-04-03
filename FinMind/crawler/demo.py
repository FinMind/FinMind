import pandas as pd

from FinMind.crawler import GovernmentBondsCrawler, CommoditiesCrawler

# -------------------------------------------------------------------
commodities_crawler = CommoditiesCrawler()
# get futures list
loop_list = commodities_crawler.create_loop_list()

# get one futures data
commodities_df = commodities_crawler.crawler(loop_list[0])

# or get all futures data
commodities_df = pd.DataFrame()
for loop in loop_list:
    print(loop)
    value = commodities_crawler.crawler(loop)
    commodities_df = commodities_df.append(value)
# -------------------------------------------------------------------
gb_crawler = GovernmentBondsCrawler()
# get futures list
loop_list = gb_crawler.create_loop_list()

# get one futures data
gd_df = gb_crawler.crawler(loop_list[0])

# or get all futures data
gd_df = pd.DataFrame()
for loop in loop_list:
    print(loop)
    value = gb_crawler.crawler(loop)
    gd_df = gd_df.append(value)
