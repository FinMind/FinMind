

<img src="https://raw.githubusercontent.com/FinMind/FinMind/master/logo.png" width="820" height="312">

[![Build Status](https://travis-ci.org/FinMind/FinMind.svg?branch=master)](https://travis-ci.org/FinMind/FinMind)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/linsamtw/FinMind/blob/master/LICENSE)
[![Documentation Status](https://readthedocs.org/projects/finminddoc/badge/?version=latest)](https://finmind.github.io/)
[![Gitter](https://badges.gitter.im/FinMindTW/community.svg)](https://gitter.im/FinMindTW/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)
[![PyPI version](https://badge.fury.io/py/FinMind.svg)](https://badge.fury.io/py/FinMind)
<!--[![Coverage Status](https://coveralls.io/repos/github/linsamtw/FinMind/badge.svg?branch=master)](https://coveralls.io/github/linsamtw/FinMind?branch=master)-->


## Quickstart
+ Refer to our [Official Documentation](https://finmind.github.io/quickstart/).

## 這是什麼?
**FinMind** 是超過 50 種金融開源數據 [50 datasets](https://finmind.github.io/)。
包含

台股股價 daily、台股 tick 交易資料（從 2019-05-29 至今，共超過三千萬筆）、財報、資產負債表、股利配息、現金流量表、月營收、外資持股、股權分散表、融資融券、三大法人買賣，台股期貨、選擇權交易明細、還原股價。

美股股價 daily、minute（從 2019-06-01至今，共超過八千萬筆），[G7](https://zh.wikipedia.org/zh-tw/%E5%85%AB%E5%A4%A7%E5%B7%A5%E6%A5%AD%E5%9C%8B%E7%B5%84%E7%B9%94) 匯率、利率。

國際原油價格、黃金價格，美債殖利率。

資料每天更新。你不需收集資料，就可進行分析。

## What is this?
**FinMind** is open source of more than [50 datasets](https://finmind.github.io/), including

Taiwan stock trade data daily, Taiwan stock trade data (5 seconds) (2019-05-29 ~ now, more than 30 million data in total), Financial Statements, Balance Sheet, Cash Flows Statement, Month Revenue, Holding Shares Per, Institutional Investors Buy Sell. Taiwan Futures Trade Detail, Taiwan Option Trade Detail.

US stock price daily, minute (2019-06-01 ~ now, more than 80 million data in total), oil price, gold price, [G7](https://zh.wikipedia.org/zh-tw/%E5%85%AB%E5%A4%A7%E5%B7%A5%E6%A5%AD%E5%9C%8B%E7%B5%84%E7%B9%94) exchange rate, interest rate.

US Government Bonds Yield.

The datasets are automatically updated daily.
You can analyze financial data without having to collect the data by yourself.

--------------

## License
- [License Detail](https://github.com/linsamtw/FinMind/blob/master/LICENSE)

## Project of Contents
- Dataset
	- [線上 API](http://api.finmindtrade.com/docs)
	- [Taiwan Stock Data](https://finmind.github.io/tutor/TaiwanMarket/DataList/)
	- [Document](https://finmind.github.io/)
	<!--- [Crawler (爬蟲)](https://github.com/FinMind/FinMind/tree/master#Crawler-爬蟲)-->
- Other
	- [Open UP Summit Slide (PPT)](https://www.slideshare.net/ssusera12be6/finmind-project-demo-199815617)
	- [Median Sharing](https://medium.com/@yanweiliu/finmind-%E4%BD%BF%E7%94%A8python%E6%9F%A5%E5%85%A8%E7%90%83%E8%82%A1%E5%83%B9-%E5%82%B5%E5%88%B8-%E5%8E%9F%E6%B2%B9%E5%83%B9%E6%A0%BC-f39d13ad6a68)
	- [HistoryUpdate](https://github.com/linsamtw/FinMind/blob/master/HistoryUpdate.md)

-------------------------------------------

## Contact
Solicit partners who are interested in joint development.

徵求有興趣共同開發的夥伴。

Email: FinMind.TW@gmail.com

每週日早上零點至早上七點為維護時間，不提供服務。

## Note
+ API Request 上限：600 / 小時。
+ Limit amount of request, 600 / hour.
+ 至[FinMind官網](https://finmindtrade.com/)註冊後，API 的 Request 加上 `user_id` 與 `password` 參數可以提高使用上限到 1500/hr。
+ `user_id` 與 `password` 參數的使用方法，可參考[線上 API](http://api.finmindtrade.com/docs)。



<!---
- [Website](https://finmindtrade.com/)
	- [Backtesting (回測)](https://github.com/FinMind/FinMind/tree/master#backtesting-回測)
	- [個股分析](https://finmindtrade.com/analysis/taiwan_stock_analysis)
-->

<!--
### Backtesting 回測

- [上傳自己設計的策略](https://finmindtrade.com/analysis/upload)，進行[線上模擬](https://finmindtrade.com/analysis/back_testing)
- 券商交易功能(開發中)，未來，使用者只需專注在策略開發上，即可利用選定策略、個股，進行自動化交易

![](https://raw.githubusercontent.com/FinMind/FinMind/master/BackTesting/online.png)

  `note` : 限制 request 上限 : 600 / hour。Limit amount of request, 600 / hour.<br>
  至[FinMind官網](https://finmindtrade.com/)註冊後，request api 帶 user_id, password 參數，使用上限可提高到 1500/hr。<br>
  user_id, password 參數使用方法，可參考[線上 api](http://api.finmindtrade.com/docs)。

### Crawler 爬蟲

- 由於原物料、債券期貨資料，有法規問題，禁止散布，因此我公開爬蟲 code，各位自行爬蟲，就不是從我這獲得資料，不會有散布問題
- [demo code](https://github.com/linsamtw/FinMind/blob/master/Crawler/demo.py)
-->
