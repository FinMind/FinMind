# 即時報價

如下程式說明如何在**盤中**獲得即時報價，主要透過 **DataSubscriber** 來進行訂閱和退訂。

在範例程式中，前部分主要說明訂閱，後部分主要說明退訂的方式。

## Demo code

#### 訂閱範例

```python
from FinMind.data import DataSubscriber
from FinMind.data import Stock
from FinMind.data import FutureAndOption


ds = DataSubscriber()

# 訂閱 2330 股票 Tick 資料
ds.subscribe("2330", Stock.Tick)

# 訂閱 2330 股票五檔報價資料
ds.subscribe("2330", Stock.BidAsk)

# 訂閱 TXFF1 期權報價
ds.subscribe("TXFF1", FutureAndOption.Tick)
```

#### 訂閱範例 + 自定 callback

```python
# 自定回調函數
def cb(message):
    stock_id = message.get("stock_id","")
    deal_price =  message.get("deal_price","")
    volume =  message.get("volume","")
    time = message.get("Time","")
    tick_type = message.get("TickType","")

    print(f"stock_id:{stock_id}, deal_price:{deal_price}, volume:{volume}, time:{time}, tick_type:{tick_type}")

# 訂閱 2330 股票 Tick 資料，使用客製化回調函數
ds.subscribe("2330", Stock.Tick, cb)

# 訂閱 2330 股票五檔報價資料，使用客製化回調函數
ds.subscribe("2330", Stock.BidAsk, cb)

# 訂閱 TXFF1 期權報價，使用客製化回調函數
ds.subscribe("TXFF1", FutureAndOption.Tick, cb)
```


#### 退訂範例
```
# 取消訂閱
ds.unsubscribe("2330",Stock.Tick)
```

## Note

- **只有在開盤的時間才有資料**
    - 早上九點到下午兩點半