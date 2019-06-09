## History Update

  ----------------------
 #### FinMind 1.0.60 (2019-05-24) 
* New data `TaiwanStockMonthRevenue`
	
		from FinMind.Data import Load
		TaiwanStockMonthRevenue = Load.FinData(
			dataset = 'TaiwanStockMonthRevenue',
			select = '2330',
			date = '2018-01-01')
* Market index:
	* TSEC weighted index ( Taiwan weighted index ) : stock_id - `^TWII`
	* SP500 : stock_id - `^GSPC`
	* Dow Jones Industrial Average : stock_id - `^DJI`

  ----------------------
 #### FinMind 1.0.57 (2019-04-28) 
* Change taiwan stock id, delete TWO and TW. ( eg. 2330.TW -> 2330 )

 #### FinMind 1.0.54 (2019-04-13) 
* Optimize speeds of loading TaiwanStockPrice, USStockPrice
* Add [DataSource](https://github.com/linsamtw/FinMind/blob/master/Data/DataSource.md)

 #### FinMind 1.0.53 (2019-04-07) 
 ##### Fix FinMind.Data.Load
 * optimize speeds of loading data , ex :
 
		from FinMind.Data import Load
		import datetime

		TaiwanStockInfo = Load.FinData(dataset = 'TaiwanStockInfo')
		s = datetime.datetime.now()
		TaiwanStockFinancialStatements = Load.FinData(dataset = 'FinancialStatements',select = list(TaiwanStockInfo['stock_id']),date = '2018-12-01')
		t = datetime.datetime.now() - s
		print(t)
		0:00:01.861724
  
 #### FinMind 1.0.52 (2019-04-06) 
 ##### New Data
 * `BalanceSheet` ( Taiwan 資產負債表 )
 * `TaiwanStockHoldingSharesPer ` ( Taiwan 股權分散表 )
 * `Shareholding` ( Taiwan 個股外資持股 )
 * `RawMaterialFuturesPrices ` ( 美國原物料期貨 )
 ##### New Function
 * `transpose(data)`
 * [demp2.py](https://github.com/linsamtw/FinMind/blob/master/demo2.py)

##### 2018/8/5
1. 央行利率 100% ( 13 Countrys, Contains G8 )

          FED Federal Reserve System 美國
          ECB European Central Bank 歐洲
          BOE Bank of England 英國
          SNB Swiss National Bank 瑞士
          RBA Reserve Bank of Australia 澳洲
          BOC Bank of Canada 加拿大
          RBNZ Reserve Bank of New Zealand 紐西蘭
          BOJ Bank of Japan 日本
          CBR The Central Bank of the Russian Federation 俄羅斯
          RBI Reserve Bank of India 印度
          PBOC People's Bank of China  中國
          BCB Banco Central do Brasil 巴西
2. Gold Price 100%
3. Government bond ->>>  https://data.oecd.org/interest/long-term-interest-rates.htm
4. 期貨 ->>> https://www.investing.com/commodities/energies
5. S&P 500指數，並爬取該 500 家股票股價 ->>>
 
##### 2018/7/5 
1. 國際油價 讀取範例 Load data example. (100%)
3. 各國匯率  ( 53 Countrys, Contains G8 )  (100%)

##### 2018/7/2 未來爬蟲順序
2. 央行利率 from https://tradingeconomics.com/search.aspx?q=Interest%20Rate
4. Inflation (通貨膨脹) monthly from https://tradingeconomics.com/russia/inflation-cpi
5. Consumer Price Index (CPI) monthly from https://tradingeconomics.com/russia/consumer-price-index-cpi
6. Output Gap monthly from https://tradingeconomics.com/russia/gdp-deflator
8. S&P 500 from yahoo finance
9. 黃金價格 from https://www.gold.org/data/gold-price




