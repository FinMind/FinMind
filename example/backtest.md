# 回測範例

如下程式說明如何使用 FinMind 進行策略回測，主要透過 **strategies** 來進行回測，**DataLoader** 讀取 FinMind 提供的資料。

在進行回測的過程中，主要要先決定回測標的、回測區間、資金部位、交易稅以及策略的設計。

回測邏輯主要是去決定**進場、維持和出場**的訊號 (signal)，例如:

    - 今天計算出來的訊號為 -1，代表明天會以開盤價**賣掉** 1 張股票
    - 今天計算出來的訊號為 0，代表明天什麼事都不做
    - 今天計算出來的訊號為 1，代表明天會以開盤價**買進** 1 張股票

回測結果提供資訊如下:

    - trade_detail: 回測詳細資料
    - compare_market_detail: 大盤累積報酬和回測累積報酬走勢
    - final_stats: 回測結果
    - compare_market_stats: 大盤年化報酬率和策略年化報酬率

在範例程式中，主要分成使用 FinMind 提供的策略和客製化策略。

## Demo code

透過 FinMind 的 [KdCrossOver 策略](https://github.com/FinMind/FinMind/blob/master/FinMind/strategies/kd_crossover.py)針對 0056 進行一年期的回測

```python
from FinMind import strategies
from FinMind.data import DataLoader

data_loader = DataLoader()
bt = strategies.BackTest(
    stock_id="0056",
    start_date="2018-01-01",
    end_date="2019-01-01",
    trader_fund=500000.0,
    fee=0.001425,
    data_loader=data_loader,
)

# 設定策略
bt.add_strategy(strategies.KdCrossOver)

# 回測
bt.simulate()

# 回測詳細資料
trade_detail = bt.trade_detail

# 大盤累積報酬和回測累積報酬走勢
compare_market_detail = bt.compare_market_detail

# 回測結果，包含總報酬(FinalProfitPer)、年化報酬(AnnualReturnPer)、最大損失(MaxLoss)、最大損失比例(MaxLossPer)...等
final_stats = bt.final_stats

# 大盤年化報酬率和策略年化報酬率
compare_market_stats = bt.compare_market_stats
```

客製化自己的策略對 0056 進行一年期的回測，客製化策略必須依照如下 **customer_strategy** class 的寫法，主要是設計 create_trade_sign 函數中的邏輯，在 stock_price dataframe 必須建立 signal 欄位，透過 signal 來決定 action (包含進場、維持還是出場)。

signal -1 為賣掉一張，1 為買進一張，0 為不做任何動作。

假設我要開發一個策略是每 30 天買進 1 張，參考如下 **customer_strategy** 策略。

```python
import pandas as pd
from FinMind import strategies
from FinMind.data import DataLoader
from FinMind.strategies.base import Strategy

class customer_strategy(Strategy):
    '''
    範例客製化策略，每 30 天買一張
    '''
    buy_freq_day = 30

    def create_trade_sign(self, stock_price: pd.DataFrame) -> pd.DataFrame:
        stock_price["signal"] = (
            stock_price.index % self.buy_freq_day == 0
        ).astype(int)
        return stock_price


data_loader = DataLoader()
bt = strategies.BackTest(
    stock_id="0056",
    start_date="2018-01-01",
    end_date="2019-01-01",
    trader_fund=500000.0,
    fee=0.001425,
    data_loader=data_loader,
)


# 設定策略
bt.add_strategy(customer_strategy)

# 回測
bt.simulate()

# 回測詳細資料
trade_detail = bt.trade_detail

# 大盤累積報酬和回測累積報酬走勢
compare_market_detail = bt.compare_market_detail

# 回測結果，包含總報酬(FinalProfitPer)、年化報酬(AnnualReturnPer)、最大損失(MaxLoss)、最大損失比例(MaxLossPer)...等
final_stats = bt.final_stats

# 大盤年化報酬率和策略年化報酬率
compare_market_stats = bt.compare_market_stats
```

## Note
