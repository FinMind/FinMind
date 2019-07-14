## History Update

--------------------------------------
 #### FinMind 1.0.80 (2019-07-15) 
 * 重大更新，過去是直接連 DataBase，目前改走 api 方式，未來舊版 package 將會失效，無法直接連 DataBase。請更新到最新版本，或是直接走 api。
 
--------------------------------------
 #### FinMind 1.0.70 (2019-06-23) 
 * add [api](https://github.com/linsamtw/FinMind/blob/master/api_demo.py)
 
--------------------------------------
 #### FinMind 1.0.62 (2019-06-10) 
* Add `Mind`, it can load all information about the Taiwan Stock, [demo](https://github.com/linsamtw/FinMind/blob/master/Mining/demo.py)<br>
e.g :

		from FinMind.Mining import Mind

		_2330 = Mind.Stock('2330','2019-01-01')
		# load Stock Price
		# load Financial Statements
		# load Share holding
		# load Institutional Investors
		# load Taiwan Stock Margin Purchase ShortSale
		# load Month Revenue
		# load Holding Shares Per
		# load Balance Sheet

		_2330.StockPrice.head()
			 date  Trading_Volume  ...         update_time  country
		0  2019-01-02        32900482  ... 2019-05-23 02:11:32   Taiwan
		1  2019-01-03        34615620  ... 2019-05-23 02:11:32   Taiwan
		2  2019-01-04        67043521  ... 2019-05-23 02:11:32   Taiwan
		3  2019-01-07        35695176  ... 2019-05-23 02:11:32   Taiwan
		4  2019-01-08        23794481  ... 2019-05-23 02:11:32   Taiwan

		_2330.FinancialStatements.head()
		   CostOfGoodsSold   EPS  FinancialCost  ...        TAX  stock_id        date
		0      128352000.0  2.37       899065.0  ...  6794340.0      2330  2019-03-31


		_2330.ShareHolding.head()
		  stock_id stock_name  ...        date         update_time
		0     2330        台積電  ...  2019-01-02 2019-06-03 15:22:18
		1     2330        台積電  ...  2019-01-03 2019-06-03 15:22:18
		2     2330        台積電  ...  2019-01-04 2019-06-03 15:22:18
		3     2330        台積電  ...  2019-01-07 2019-06-03 15:22:18
		4     2330        台積電  ...  2019-01-08 2019-06-03 15:22:18

		_2330.InstitutionalInvestors.head()
				  name       buy  ...  country         update_time
		0       Dealer_Hedging    183000  ...   Taiwan 2019-05-23 02:07:21
		1          Dealer_self    742000  ...   Taiwan 2019-05-23 02:07:21
		2  Foreign_Dealer_Self         0  ...   Taiwan 2019-05-23 02:07:21
		3     Foreign_Investor  13633825  ...   Taiwan 2019-05-23 02:07:21
		4     Investment_Trust    175000  ...   Taiwan 2019-05-23 02:07:21

		_2330.MarginPurchaseShortSale.head()
		  stock_id stock_name  MarginPurchaseBuy  ...  Note        date         update_time
		0     2330        台積電               1013  ...  None  2019-01-02 2019-05-23 02:10:57
		1     2330        台積電                830  ...  None  2019-01-03 2019-05-23 02:10:57
		2     2330        台積電               2153  ...  None  2019-01-04 2019-05-23 02:10:57
		3     2330        台積電                296  ...  None  2019-01-07 2019-05-23 02:10:57
		4     2330        台積電                264  ...  None  2019-01-08 2019-05-23 02:10:57

		_2330.MonthRevenue.head()
		  stock_id      revenue  revenue_year  ...        date country         update_time
		0     2330  89830598000          2018  ...  2019-01-01  Taiwan 2019-05-23 03:32:05
		1     2330  78093827000          2019  ...  2019-02-01  Taiwan 2019-05-23 09:54:08
		2     2330  60889055000          2019  ...  2019-03-01  Taiwan 2019-05-23 09:54:15
		3     2330  79721587000          2019  ...  2019-04-01  Taiwan 2019-05-23 09:54:33
		4     2330  74693615000          2019  ...  2019-05-01  Taiwan 2019-05-23 09:54:32

		_2330.HoldingSharesPer.head()

		  HoldingSharesLevel  people  ...        date         update_time
		0              1-999  144921  ...  2019-01-19 2019-05-23 02:06:36
		1        1,000-5,000  153113  ...  2019-01-19 2019-05-23 02:06:36
		2      10,001-15,000    9248  ...  2019-01-19 2019-05-23 02:06:36
		3    100,001-200,000    1585  ...  2019-01-19 2019-05-23 02:06:36
		4      15,001-20,000    4411  ...  2019-01-19 2019-05-23 02:06:36


		_2330.BalanceSheet.head()

			 date stock_id  ...         value         update_time
		0  2019-03-31     2330  ...  2.710090e+10 2019-05-23 02:03:23
		1  2019-03-31     2330  ...  1.240000e+00 2019-05-23 02:03:23
		2  2019-03-31     2330  ...  5.609410e+08 2019-05-23 02:03:23
		3  2019-03-31     2330  ...  3.000000e-02 2019-05-23 02:03:23
		4  2019-03-31     2330  ...  3.098210e+08 2019-05-23 02:03:23

		_2330.StockPrice['move_average'] = Mind.MoveAverage(_2330.StockPrice,days = 5,variable = 'close')
		_2330.StockPrice['RSV'] = Mind.RSV(_2330.StockPrice,days = 5)
		_2330.StockPrice['BIAS'] = Mind.BIAS(_2330.StockPrice,days = 5)
		
		_2330.StockPrice.head()
			 date  Trading_Volume  Trading_money  ...  move_average   RSV  BIAS
		0  2019-01-02        32900482     7276419230  ...           NaN   NaN   NaN
		1  2019-01-03        34615620     7459051790  ...           NaN   NaN   NaN
		2  2019-01-04        67043521    13987136785  ...           NaN   NaN   NaN
		3  2019-01-07        35695176     7591116569  ...           NaN   NaN   NaN
		4  2019-01-08        23794481     5019703557  ...         213.4  22.0 -1.12

* add function `Mind.MoveAverage`, <br>
e.g : 
		
		Mind.MoveAverage(_2330.StockPrice,days = 5,variable = 'close')
		
* add function `Mind.RSV`, <br>
e.g : 
	
		Mind.RSV(_2330.StockPrice,days = 5)
	
* add function `Mind.BIAS`, <br>
e.g : 
	
		Mind.BIAS(_2330.StockPrice,days = 5)

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




