<p align="center">
  <img src="https://raw.githubusercontent.com/FinMind/FinMind/master/logo.png" width="820" height="312">
</p>

<p align="center">
  <a href="https://travis-ci.org/FinMind/FinMind"><img src="https://travis-ci.org/FinMind/FinMind.svg?branch=master" alt="Build Status"></a>
  <a href="https://github.com/linsamtw/FinMind/blob/master/LICENSE"><img src="https://img.shields.io/github/license/FinMind/FinMind" alt="license"></a>
  <a href="https://finmind.github.io/"><img src="https://readthedocs.org/projects/finminddoc/badge/?version=latest" alt="Documentation Status"></a>
  <a href="https://gitter.im/FinMindTW/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge"><img src="https://badges.gitter.im/FinMindTW/community.svg" alt="Gitter"></a>
  <a href="https://badge.fury.io/py/FinMind"><img src="https://badge.fury.io/py/FinMind.svg" alt="PyPI version"></a>
  <!--<a href="https://coveralls.io/github/linsamtw/FinMind?branch=master"><img src="https://coveralls.io/repos/github/linsamtw/FinMind/badge.svg?branch=master" alt="Coverage Status"></a>-->
</p>

## Donate

* [贊助我們發展更多功能](https://finmindtrade.com/analysis/#/Sponsor/sponsor)

<a href="https://finmindtrade.com/analysis/#/Sponsor/sponsor"><img src="https://payment.ecpay.com.tw/Content/themes/WebStyle20170517/images/ecgo.png" alt=""/></a>

## Quickstart

+ Refer to our [Official Documentation](https://finmind.github.io/quickstart/).

## 這是什麼?

**FinMind** 是超過 50 種金融開源數據 [50 datasets](https://finmind.github.io/)。
包含

* 技術面 : 台股股價 daily、即時報價、歷史 tick、即時最佳五檔、PER、PBR、每5秒委託成交統計、加權指數、當日沖銷交易標的及成交量值。
* 基本面 : 綜合損益表、現金流量表、資產負債表、股利政策表、除權除息結果表、月營收。
* 籌碼面 : 外資持股、股權分散表、融資融券、三大法人買賣、借券成交明細。
* 消息面 : 台股相關新聞。
* 衍生性商品 : 期貨、選擇權 daily data、即時報價、交易明細，選擇權、期貨三大法人買賣，期貨各卷商每日交易、選擇權各卷商每日交易。
* 國際市場 : 美股股價 daily、minute、美國債券殖利率、貨幣發行量(美國)、黃金價格、原油價格、G8 央行利率、G8 匯率、

資料每天更新。你不需收集資料，就可進行分析。

## What is this?

**FinMind** is open source of more than [50 datasets](https://finmind.github.io/), including

Taiwan stock trade data daily, Taiwan stock trade data (5 seconds) (2019-05-29 ~ now, more than 30 million data in
total), Financial Statements, Balance Sheet, Cash Flows Statement, Month Revenue, Holding Shares Per, Institutional
Investors Buy Sell. Taiwan Futures Trade Detail, Taiwan Option Trade Detail.

US stock price daily, minute (2019-06-01 ~ now, more than 80 million data in total), oil price, gold
price, [G7](https://zh.wikipedia.org/zh-tw/%E5%85%AB%E5%A4%A7%E5%B7%A5%E6%A5%AD%E5%9C%8B%E7%B5%84%E7%B9%94) exchange
rate, interest rate.

US Government Bonds Yield.

The datasets are automatically updated daily. You can analyze financial data without having to collect the data by
yourself.

--------------

## License

- [License Detail](https://github.com/linsamtw/FinMind/blob/master/LICENSE)

- 資料來源:
  [證交所](https://www.twse.com.tw/zh/), [櫃買中心](https://www.tpex.org.tw/web/)
  , [公開資訊觀測站](https://mops.twse.com.tw/mops/web/index), [期交所](https://www.taifex.com.tw/cht/index)。
- 本專案提供的所有內容均用於教育、非商業用途。資料僅供參考，使用者依本資料交易發生交易損失需自行負責，本專案不對資料內容錯誤、更新延誤或傳輸中斷負任何責任。

## Project of Contents

- Dataset
  - [線上 API](http://api.finmindtrade.com/docs)
  - [Taiwan Stock Data](https://finmind.github.io/tutor/TaiwanMarket/DataList/)
  - [Document](https://finmind.github.io/)
  - [壓力測試](https://finmind.github.io/StressTest/)
  <!--- [Crawler (爬蟲)](https://github.com/FinMind/FinMind/tree/master#Crawler-爬蟲)-->


- Other
    - [Open UP Summit Slide (PPT)](https://www.slideshare.net/ssusera12be6/finmind-project-demo-199815617)
    - [Median Sharing](https://medium.com/@yanweiliu/finmind-%E4%BD%BF%E7%94%A8python%E6%9F%A5%E5%85%A8%E7%90%83%E8%82%A1%E5%83%B9-%E5%82%B5%E5%88%B8-%E5%8E%9F%E6%B2%B9%E5%83%B9%E6%A0%BC-f39d13ad6a68)
    - [HistoryUpdate](https://github.com/linsamtw/FinMind/blob/master/HistoryUpdate.md)

-------------------------------------------

## Contact

<!-- Solicit partners who are interested in joint development.

徵求有興趣共同開發的夥伴。 -->

Email: FinMind.TW@gmail.com

每週日早上零點至早上七點為維護時間，不提供服務。

## Note
+ 未來預計新增更多功能，包含個人化回測分析、chatbot 監控策略，
+ API Request 上限：300 / 小時。
+ Limit amount of request, 300 / hour. 
+ 至[FinMind官網](https://finmindtrade.com/)註冊並驗證信箱後，API 的 Request 加上 `token` 參數可以提高使用上限到 600/hr。
+ `token` 獲取方法，可在[官網](https://finmindtrade.com/analysis/#/account/login)登入後獲取。

=======
<p align="center">
  <img src="https://raw.githubusercontent.com/FinMind/FinMind/master/logo.png" width="820" height="312">
</p>

<p align="center">
  <a href="https://travis-ci.org/FinMind/FinMind"><img src="https://travis-ci.org/FinMind/FinMind.svg?branch=master" alt="Build Status"></a>
  <a href="https://github.com/linsamtw/FinMind/blob/master/LICENSE"><img src="https://img.shields.io/github/license/FinMind/FinMind" alt="license"></a>
  <a href="https://finmind.github.io/"><img src="https://readthedocs.org/projects/finminddoc/badge/?version=latest" alt="Documentation Status"></a>
  <a href="https://gitter.im/FinMindTW/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge"><img src="https://badges.gitter.im/FinMindTW/community.svg" alt="Gitter"></a>
  <a href="https://badge.fury.io/py/FinMind"><img src="https://badge.fury.io/py/FinMind.svg" alt="PyPI version"></a>
  <!--<a href="https://coveralls.io/github/linsamtw/FinMind?branch=master"><img src="https://coveralls.io/repos/github/linsamtw/FinMind/badge.svg?branch=master" alt="Coverage Status"></a>-->
</p>

## Donate

* [贊助我們發展更多功能 (金額由你決定)](https://p.ecpay.com.tw/8196A98)

<a href="https://p.ecpay.com.tw/8196A98"><img src="https://payment.ecpay.com.tw/Content/themes/WebStyle20170517/images/ecgo.png" alt=""/></a>

## Quickstart

+ Refer to our [Official Documentation](https://finmind.github.io/quickstart/).

## Example

```python
# 取得還原股價
from FinMind.data import DataLoader

dl = DataLoader()
adj_price = dl.stock_adj_price("2330", "2018-01-01", "2021-03-03")

# 繪製k線圖
from FinMind import plotting

plotting.kline(adj_price)
```

<div style="text-align: center">
<img src="https://s3.us-west-2.amazonaws.com/secure.notion-static.com/680988a6-7c5b-4925-9f62-b40209bcd89f/kline_demo2.gif?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45O3KS52Y5%2F20210404%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20210404T044414Z&X-Amz-Expires=86400&X-Amz-Signature=8785982a514dc95d93e3f7abc485a4b111710c803c3d6a64c8574b3964715943&X-Amz-SignedHeaders=host" alt="drawing" width="600"/>
</div>

## 這是什麼?

**FinMind** 是超過 50 種金融開源數據 [50 datasets](https://finmind.github.io/)。
包含

* 技術面 : 台股股價 daily、即時報價、歷史 tick、即時最佳五檔、PER、PBR、每5秒委託成交統計、加權指數、當日沖銷交易標的及成交量值。
* 基本面 : 綜合損益表、現金流量表、資產負債表、股利政策表、除權除息結果表、月營收。
* 籌碼面 : 外資持股、股權分散表、融資融券、三大法人買賣、借券成交明細。
* 消息面 : 台股相關新聞。
* 衍生性商品 : 期貨、選擇權 daily data、即時報價、交易明細，選擇權、期貨三大法人買賣，期貨各卷商每日交易、選擇權各卷商每日交易。
* 國際市場 : 美股股價 daily、minute、美國債券殖利率、貨幣發行量(美國)、黃金價格、原油價格、G8 央行利率、G8 匯率、

資料每天更新。你不需收集資料，就可進行分析。

## What is this?

**FinMind** is open source of more than [50 datasets](https://finmind.github.io/), including

Taiwan stock trade data daily, Taiwan stock trade data (5 seconds) (2019-05-29 ~ now, more than 30 million data in
total), Financial Statements, Balance Sheet, Cash Flows Statement, Month Revenue, Holding Shares Per, Institutional
Investors Buy Sell. Taiwan Futures Trade Detail, Taiwan Option Trade Detail.

US stock price daily, minute (2019-06-01 ~ now, more than 80 million data in total), oil price, gold
price, [G7](https://zh.wikipedia.org/zh-tw/%E5%85%AB%E5%A4%A7%E5%B7%A5%E6%A5%AD%E5%9C%8B%E7%B5%84%E7%B9%94) exchange
rate, interest rate.

US Government Bonds Yield.

The datasets are automatically updated daily. You can analyze financial data without having to collect the data by
yourself.

--------------

## License

- [License Detail](https://github.com/linsamtw/FinMind/blob/master/LICENSE)

- 資料來源:
  [證交所](https://www.twse.com.tw/zh/), [櫃買中心](https://www.tpex.org.tw/web/)
  , [公開資訊觀測站](https://mops.twse.com.tw/mops/web/index), [期交所](https://www.taifex.com.tw/cht/index)。
- 本專案提供的所有內容均用於教育、非商業用途。資料僅供參考，使用者依本資料交易發生交易損失需自行負責，本專案不對資料內容錯誤、更新延誤或傳輸中斷負任何責任。

## Project of Contents

- Dataset
    - [線上 API](http://api.finmindtrade.com/docs)
    - [Taiwan Stock Data](https://finmind.github.io/tutor/TaiwanMarket/DataList/)
    - [Document](https://finmind.github.io/)
  <!--- [crawler (爬蟲)](https://github.com/FinMind/FinMind/tree/master#Crawler-爬蟲)-->

- Other
    - [Open UP Summit Slide (PPT)](https://www.slideshare.net/ssusera12be6/finmind-project-demo-199815617)
    - [Median Sharing](https://medium.com/@yanweiliu/finmind-%E4%BD%BF%E7%94%A8python%E6%9F%A5%E5%85%A8%E7%90%83%E8%82%A1%E5%83%B9-%E5%82%B5%E5%88%B8-%E5%8E%9F%E6%B2%B9%E5%83%B9%E6%A0%BC-f39d13ad6a68)
    - [HistoryUpdate](https://github.com/linsamtw/FinMind/blob/master/HistoryUpdate.md)

## Contact

<!-- Solicit partners who are interested in joint development.

徵求有興趣共同開發的夥伴。 -->

Email: FinMind.TW@gmail.com

每週日早上零點至早上七點為維護時間，不提供服務。

## Note

+ 未來預計新增更多功能，包含個人化回測分析、chatbot 監控策略，因此 4/11 之後會更改使用方案，並增加 backer、sponsor 兩種贊助方案，
+ API Request 上限：600 / 小時。(4/11後，300/hr)
+ Limit amount of request, 600 / hour. (After 4/11，300/hr)
+ 至[FinMind官網](https://finmindtrade.com/)註冊並驗證信箱後，API 的 Request 加上 `user_id` 與 `password` 參數可以提高使用上限到 1500/hr。(
  4/11後，600/hr)
+ `user_id` 與 `password` 參數的使用方法，可參考[線上 API](http://api.finmindtrade.com/docs)。