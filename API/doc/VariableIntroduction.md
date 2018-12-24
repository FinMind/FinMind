# Variable Introduction

### 1. Taiwan Stock Info
###### 1815 檔股票

| variable name | 變數名稱 | example |
|---------------|---------|----------|
| stock_id | 股票代號 | 1101 |
| stock_name | 股票中文名 | 台泥 |
| stock_class | 股票產業類別 | 水泥工業 |
| id | 索引 | 1 |

資料來源 :  <br>
https://goodinfo.tw/StockInfo/StockList.asp


<html>
<p align="right">
  <a href = 'https://github.com/linsamtw/FinancialMining/tree/master/OpenData#variable-introduction'> Home </a></p>
</html>

------------------------------------------------------------
### 2. Taiwan Stock Prices 
###### 1815 檔股票

| variable name | 變數名稱 | example |
|---------------|---------|----------|
|Date|日期| 2008-01-02 |
| stock_id | 股票代號, 以 [yahoo finance](https://finance.yahoo.com/) 為準 | 台股 0050 -> 美股 0050.TW |
| Open | 開盤 | 60.1 |
| High | 最高 | 61.3  |
| Low | 最低 | 60 |
| Close | 收盤 | 60.1 |
| Adj_Close  | 調整後的收盤價 | 57.2 |
| Volume | 成交量 | 4975000 |
| id | 索引 | 1 |

資料來源 :  <br>
https://finance.yahoo.com/

<html>
<p align="right">
  <a href = 'https://github.com/linsamtw/FinancialMining/tree/master/OpenData#variable-introduction'> Home </a></p>
</html>

------------------------------------------------------------
### 3. Taiwan Stock Financial Statements
###### 1667 檔股票 ( 部分股票無財報 )，89635 筆 data

| variable name | 變數名稱 | example |
|---------------|---------|----------|
| BTAXM (Income before Tax Margin) | 稅前純益 | 0.1602 |
| COST (Cost of Goods Sold or Manufacturing)|營業成本|3963330|
| EPS (Earnings Per Share) |每股盈餘|0.17|
|GM  (Gross margin)|毛利率|0.1056|
|NI (Net Income)|稅後淨利|275033|
|BTAX (Income before Tax)|稅前純益|710033|
|NIM  ( Net Profit Margin)|純益率|0.0621|
|OE (Operating Expenses)|營業費用|260302|
|OI (Operating Income)|營業淨利|207582|
|OIM  (Operating Profit Margin)|營業利益率|0.0468|
|PRO (Gross Profit)|營業毛利|467884|
|REV (Gross Revenue)|營業收入|4431220|
|TAX (Income Tax Expense)|所得稅費用|435000|
|stock_id|股票代號|1101|
|year|年|1997|
|quar|季|4|
|url|資料來源|https://stock.wearn.com/Income_detial.asp?kind=1101&y=8604|

資料來源 : <br>
https://stock.wearn.com/Income.asp <br>
http://www.tedc.org.tw/tedc/bank/otccomp/ch1.3.4.htm

<html>
<p align="right">
  <a href = 'https://github.com/linsamtw/FinancialMining/tree/master/OpenData#variable-introduction'> Home </a></p>
</html>

------------------------------------------------------------
### 4. Taiwan Stock Dividend 
###### 1815 檔股票，25,330 筆 data

| variable name | 變數名稱 | example |
|---------------|---------|----------|
|Shareholders meeting date|股東會日期|2010-06-15|
|Retained_Earnings |盈餘配股(元/股)|0|
|Capital_Reserve|公積配股(元/股)|0|
|Ex_right_trading_day|除權交易日|None|
|total employee bonus stock shares|員工配股(總張數)|0|
|Cash dividend|現金股利|3|
|Ex-dividend transaction day|除息交易日|2010-07-06|
|total employee bonus shares|員工紅利(總金額)|6.69134e+06|
|Directors remuneration|董監酬勞 |67692|
|stock_id|股票代號|2330|

資料來源 : <br>
https://stock.wearn.com/dividend.asp

<html>
<p align="right">
  <a href = 'https://github.com/linsamtw/FinancialMining/tree/master/OpenData#variable-introduction'> Home </a></p>
</html>

------------------------------------------------------------
### 5. Taiwan Stock Institutional Investors
###### 2004 ~ now

| variable name | 變數名稱 | example |
|---------------|---------|----------|
|Dealer_buy|自營商 買進金額|62.63|
|Dealer_sell |自營商 賣出金額|75.16|
|Investment_Trust_buy|投信 買進金額|8.97|
|Investment_Trust_sell|投信 賣出金額|8.4|
|Foreign_Investor_buy|外資 買進金額|244.37|
|Foreign_Investor_sell|外資 賣出金額|169.216|
|total_buy|合計 買進金額|315.97|
|total_sell|合計 賣出金額|252.77|
|date|交易日期|2016-02-25|

資料來源 : <br>
https://stock.wearn.com/fundthree.asp?mode=search

<html>
<p align="right">
  <a href = 'https://github.com/linsamtw/FinancialMining/tree/master/OpenData#variable-introduction'> Home </a></p>
</html>

------------------------------------------------------------
### 6. Crude Oil Prices
###### 1986 ~ now

| variable name | 變數名稱 | example (單位: 美金) |
|---------------|---------|----------|
|WTI|西德州|26.4|
|Brent|布蘭特|22.57|
|date|日期|2000-01-01|
 
資料來源 : <br>
https://www.eia.gov/dnav/pet/pet_pri_spt_s1_d.htm

<html>
<p align="right">
  <a href = 'https://github.com/linsamtw/FinancialMining/tree/master/OpenData#variable-introduction'> Home </a></p>
</html>

------------------------------------------------------------
### 7. Exchange Rate 
###### 2000 ~ now

| variable name | 變數名稱 | example (以美金為主要兌換匯率) |
|---------------|---------|----------|
|InterbankRate|銀行間利率|26.11 ( 26.11 TWD : 1 US ) |
|InverseInterbankRate|反向銀行間利率|0.0383 ( 1 TWD : 0.0383 US )|
|country|國家|TWD Taiwanese New Dollar|
|date|日期|1990-01-03|

資料來源 : <br>
https://www.ofx.com/en-au/forex-news/historical-exchange-rates/

<html>
<p align="right">
  <a href = 'https://github.com/linsamtw/FinancialMining/tree/master/OpenData#variable-introduction'> Home </a></p>
</html>

------------------------------------------------------------
### 8. Interest Rate 
###### 2000 ~ now

| variable name | 變數名稱 | example |
|---------------|---------|----------|
|interest_rate|銀行利率|10.25 |
|full_country_name|國家全名|Federal_Reserve|
|country|國家|FED|
|date|日期|1982-09-27|
 
資料來源 : <br>
https://www.investing.com/central-banks

<html>
<p align="right">
  <a href = 'https://github.com/linsamtw/FinancialMining/tree/master/OpenData#variable-introduction'> Home </a></p>
</html>

------------------------------------------------------------
### 9. Gold Price
###### 1979 ~ now

| variable name | 變數名稱 | example |
|---------------|---------|----------|
|datetime|date time (after 2018/01/01, data is minutely)|1978-12-29 00:00:00 |
|Price|gold price ( US/Oz )|226.0|
 
資料來源 : <br>
https://www.gold.org/data/gold-price

<html>
<p align="right">
  <a href = 'https://github.com/linsamtw/FinancialMining/tree/master/OpenData#variable-introduction'> Home </a></p>
</html>

------------------------------------------------------------
### 10. Government Bonds
###### 1980 ~ now

| variable name | 變數名稱 | example |
|---------------|---------|----------|
|Date|date time |2013-10-29 |
|Price|Bond Yield |0.895|
|Open|Bond Yield |0.88|
|High|Bond Yield |0.9|
|Low|Bond Yield |0.88|
|ChangePercent|Bond Yield |0.0113|
|data_name|Bonds kinds|1-Month|
|country|country|Canada|
 
資料來源 : <br>
https://www.investing.com/rates-bonds/

<html>
<p align="right">
  <a href = 'https://github.com/linsamtw/FinancialMining/tree/master/OpenData#variable-introduction'> Home </a></p>
</html>

------------------------------------------------------------
### 11. Energy Futures Prices

| variable name | example |
|---------------|----------|
|Date |2018-08-09 |
|Price| |72.07|
|Open |72.16|
|High|72.89|
|Low|71.86|
|Vol|197060|
|ChangePercent|-0.0029|
|data_name|Brent Oil Futures|
 
資料來源 : <br>
https://www.investing.com/commodities/energies

<html>
<p align="right">
  <a href = 'https://github.com/linsamtw/FinancialMining/tree/master/OpenData#variable-introduction'> Home </a></p>
</html>





