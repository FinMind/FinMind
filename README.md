[![Build Status](https://travis-ci.org/linsamtw/FinMind.svg?branch=master)](https://travis-ci.org/linsamtw/FinMind)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/linsamtw/FinMind/blob/master/LICENSE)
[![PyPI version](https://badge.fury.io/py/FinMind.svg)](https://badge.fury.io/py/FinMind)
[![Documentation Status](https://readthedocs.org/projects/finminddoc/badge/?version=latest)](https://finminddoc.readthedocs.io/en/latest/?badge=latest)
<!--[![Coverage Status](https://coveralls.io/repos/github/linsamtw/FinMind/badge.svg?branch=master)](https://coveralls.io/github/linsamtw/FinMind?branch=master)-->

-----------------------
Solicit partners who are interested in joint development. <br>
徵求有興趣共同開發的夥伴。<br>
My email : linsam.tw.github@gmail.com

-----------------------

You can analyze financial data without having to collect the data by yourself. The datasets are automatically updated daily.

     pip3 install FinMind
     
 ---------------------
 The full version of this documentation is at [https://linsamtw.github.io/FinMindDoc/](https://linsamtw.github.io/FinMindDoc/).
 
 Financial Visualize [http://finmind.servebeer.com/](http://finmind.servebeer.com/) (In development)
 
 [40 data sets](https://github.com/linsamtw/FinMind/blob/master/dataset.md)

  ----------------------
  # [FinMind.Data](https://github.com/linsamtw/FinMind/tree/master/Data)
  
  # [FinMind.Mind](https://github.com/linsamtw/FinMind/tree/master/Mining)
  
   ----------------------
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

[HistoryUpdate](https://github.com/linsamtw/FinMind/blob/master/HistoryUpdate.md)

 ----------------------

### Financial Visualize ( In development )
At least five kinds of visualization tools for every data type. ( In development )<br>
[http://finmind.servebeer.com/](http://finmind.servebeer.com/)
開發中

------------------------------------------------------------
### [License](https://github.com/linsamtw/FinMind/blob/master/LICENSE)


email : linsam.tw.github@gmail.com


