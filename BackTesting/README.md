

## 回測系統

#### [ 線上回測系統 ](https://finmindtrade.com/analysis/back_testing)

可[上傳自己設計的策略](https://finmindtrade.com/analysis/upload)，進行[線上模擬](https://finmindtrade.com/analysis/back_testing)。<br>
卷商交易功能(開發中)，未來，使用者只需專注在策略開發上，即可利用選定策略、個股，進行自動化交易。<br>

![](https://raw.githubusercontent.com/FinMind/FinMind/master/BackTesting/online.png)

策略上傳範例，可使用[線下開發](https://github.com/FinMind/FinMind/blob/master/BackTesting/test.ipynb)，進行線下測試，範例如下。


    import pandas as pd
    import numpy as np
    import requests

    # class name，必須跟檔案名一致，例如 class demo，檔名也是 demo.py
    class demo:
        def __init__(self,
                     stock_price,
                     **kwargs,):
            #-------------------------------------------------------------------    
            # 此區塊請勿更動
            stock_price = stock_price.sort_values('date')
            # 股價
            self.stock_price = stock_price
            # 融資融券
            self.MarginPurchaseShortSale = kwargs.get("MarginPurchaseShortSale", pd.DataFrame())
            # 三大法人買賣
            self.InstitutionalInvestorsBuySell = kwargs.get("InstitutionalInvestorsBuySell", pd.DataFrame())
            # 外資持股
            self.Shareholding = kwargs.get("Shareholding", pd.DataFrame())
            # 此區塊請勿更動
            #-------------------------------------------------------------------

        def trade(self,date):
            ''' 
            此區塊，可進行資料處理、做技術指標，寫自己的策略，
            寫你自己的策略, 必須 return : 1 (買) or -1 (賣) or 0 (不操作)
            根據date，回傳當下要進行什麼操作 ( 買/賣/不操作 )
            
            date : 昨天時間
            用昨天的資料，計算技術指標，判斷今天買/賣
            '''
            # example
            from random import randint

            x = randint(1,10)
            x = x%3
            if x == 1:
                return 1
            elif x == 2:
                return -1
            elif x == 0:
                return 0


[demo](https://github.com/FinMind/FinMind/blob/master/BackTesting/demo.py)<br>
[BAIS](https://github.com/FinMind/FinMind/blob/master/BackTesting/BAIS.py)<br>
[KD](https://github.com/FinMind/FinMind/blob/master/BackTesting/KD.py)



#### [線下開發](https://github.com/FinMind/FinMind/blob/master/BackTesting/test.ipynb)

![](https://raw.githubusercontent.com/FinMind/FinMind/master/BackTesting/offline.png)
UnrealizedProfit : 未實現損益<br>
realizedProfit : 已實現損益<br>
everytime_profit : 當下結算獲利<br>


