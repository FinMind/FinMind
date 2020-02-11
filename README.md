[![Build Status](https://travis-ci.org/FinMind/FinMind.svg?branch=master)](https://travis-ci.org/FinMind/FinMind)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/linsamtw/FinMind/blob/master/LICENSE)
[![PyPI version](https://badge.fury.io/py/FinMind.svg)](https://badge.fury.io/py/FinMind)
[![Documentation Status](https://readthedocs.org/projects/finminddoc/badge/?version=latest)](https://finminddoc.readthedocs.io/en/latest/?badge=latest)
<!--[![Coverage Status](https://coveralls.io/repos/github/linsamtw/FinMind/badge.svg?branch=master)](https://coveralls.io/github/linsamtw/FinMind?branch=master)-->

## 這是什麼?
**FinMind** 是超過 50 種金融開源數據 [50 datasets](https://github.com/linsamtw/FinMind/blob/master/dataset.md)。
包含

台股股價 daily、台股5秒交易資料 ( 2019-05-29 ~ now, 共超過 3 千萬筆 )、財報、資產負債表、股利配息、現金流量表、月營收、外資持股、股權分散表、融資融券、三大法人買賣，台股期貨、選擇權交易明細、還原股價。

美股股價 daily、minute ( 2019-06-01 ~ now, 共超過 8 千萬筆 )，[G7](https://zh.wikipedia.org/zh-tw/%E5%85%AB%E5%A4%A7%E5%B7%A5%E6%A5%AD%E5%9C%8B%E7%B5%84%E7%B9%94) 匯率、利率。<br>
國際原油價格、黃金價格，美債殖利率。

資料每天更新。你不需收集資料，就可進行分析。

## What is it?
**FinMind** is open source of more than [50 datasets](https://github.com/linsamtw/FinMind/blob/master/dataset.md)  , contain

Taiwan stock trade data daily, Taiwan stock trade data (5 seconds) ( 2019-05-29 ~ now, total more than 30 million data ), Financial Statements, Balance Sheet, Cash Flows Statement, Month Revenue, Holding Shares Per, Institutional Investors Buy Sell. Taiwan Futures Trade Detail, Taiwan Option Trade Detail.

US stock price daily, minute ( 2019-06-01 ~ now, total more than 80 million data ), oil price, gold price, [G7](https://zh.wikipedia.org/zh-tw/%E5%85%AB%E5%A4%A7%E5%B7%A5%E6%A5%AD%E5%9C%8B%E7%B5%84%E7%B9%94) exchange rate, interest rate. <br>
US Government Bonds Yield.

The datasets are automatically updated daily.
You can analyze financial data without having to collect the data by yourself.<br>

     pip3 install FinMind

Solicit partners who are interested in joint development. <br>
徵求有興趣共同開發的夥伴。<br>
email : FinMind.TW@gmail.com

-------------------------------------------
## License

- [License Detail](https://github.com/linsamtw/FinMind/blob/master/LICENSE)

## Project of Contents

- [Website](https://finmindtrade.com/)
	- [Backtesting (回測)](https://github.com/FinMind/FinMind#Backtesting&emsp;(回測))
	- [個股分析](https://finmindtrade.com/analysis/taiwan_stock_analysis)

- Dataset
	- [Dataset Api](https://github.com/FinMind/FinMind#Dataset&emsp;Api)
	- [中英對照表](https://github.com/FinMind/FinMind/blob/master/VariableDocument.md)
	- [Crawler (爬蟲)]()

- Other

	- The full version of this [documentation](https://linsamtw.github.io/FinMindDoc/)

	- [Median Sharing](https://medium.com/@yanweiliu/finmind-%E4%BD%BF%E7%94%A8python%E6%9F%A5%E5%85%A8%E7%90%83%E8%82%A1%E5%83%B9-%E5%82%B5%E5%88%B8-%E5%8E%9F%E6%B2%B9%E5%83%B9%E6%A0%BC-f39d13ad6a68)

	- [HistoryUpdate](https://github.com/linsamtw/FinMind/blob/master/HistoryUpdate.md)

	- [Open UP Summit Slide(PPT)](https://www.slideshare.net/ssusera12be6/finmind-project-demo-199815617)



### Backtesting (回測)

- [上傳自己設計的策略](https://finmindtrade.com/analysis/upload)，進行[線上模擬](https://finmindtrade.com/analysis/back_testing)
- 券商交易功能(開發中)，未來，使用者只需專注在策略開發上，即可利用選定策略、個股，進行自動化交易

![](https://raw.githubusercontent.com/FinMind/FinMind/master/BackTesting/online.png)

### Dataset Api

- [Data sets list](https://github.com/linsamtw/FinMind/blob/master/dataset.md)

- [Python dataset api document](https://github.com/linsamtw/FinMind/blob/master/example/Python%20document.md)

```
import requests
url = 'http://finmindapi.servebeer.com/api/data'
form_data = {'dataset':'TaiwanStockInfo'}
res = requests.post(url,verify = True,data = form_data)

url = 'http://finmindapi.servebeer.com/api/data'
form_data = {'dataset':'TaiwanStockPrice','stock_id':'2317','date':'2019-06-01'}
res = requests.post(url,verify = True,data = form_data)

temp = res.json()
data = pd.DataFrame(temp['data'])
data.head()
```

  * [R document](https://github.com/linsamtw/FinMind/blob/master/example/R%20document.md)

```
library(httr)
library(jsonlite)
library('data.table')
library(dplyr)

url = 'http://finmindapi.servebeer.com/api/data'

# TaiwanStockInfo
payload<-list( 'dataset' = 'TaiwanStockInfo')

response = POST(url,body = payload,encode="json")
data = response %>% content
data = do.call('cbind',data$data) %>%data.table
head(data)
```

  `note` : 限制 request 上限 : 600 / hour。Limit amount of request, 600 / hour.<br>
  至[官網](https://finmindtrade.com/)註冊後，request api 帶 user_id, password 參數，使用上限可提高到 1500/hr。<br>
  user_id, password 參數使用方法，可參考[線上 api](http://finmindapi.servebeer.com/docs#/default/data_api_data_post)。

## translation 中英對照

- [中英對照 Document](https://github.com/linsamtw/FinMind/blob/master/VariableDocument.md)

- 中英對照 api

```
import requests
url = 'http://finmindapi.servebeer.com/api/translation'
dataset = 'RawMaterialFuturesPrices'
# or
# dataset = 'FinancialStatements'
# dataset = 'BalanceSheet'
# dataset = 'StockDividend'
# dataset = 'TaiwanStockMarginPurchaseShortSale'
# dataset = 'InstitutionalInvestorsBuySell'
parameter = {'dataset':dataset}

res = requests.post(url,verify = True,data = parameter)
#res.text
data = res.json()
data = pd.DataFrame( data['data'] )
```

### Crawler (爬蟲)

- 由於原物料、債券期貨資料，有法規問題，禁止散布，因此我公開爬蟲 code，各位自行爬蟲，就不是從我這獲得資料，不會有散布問題
- [demo code](https://github.com/linsamtw/FinMind/blob/master/Crawler/demo.py)