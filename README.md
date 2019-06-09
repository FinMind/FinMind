[![Build Status](https://travis-ci.org/linsamtw/FinMind.svg?branch=master)](https://travis-ci.org/linsamtw/FinMind)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/linsamtw/FinMind/blob/master/LICENSE)
[![PyPI version](https://badge.fury.io/py/FinMind.svg)](https://badge.fury.io/py/FinMind)
[![Documentation Status](https://readthedocs.org/projects/finminddoc/badge/?version=latest)](https://finminddoc.readthedocs.io/en/latest/?badge=latest)
<!--[![Coverage Status](https://coveralls.io/repos/github/linsamtw/FinMind/badge.svg?branch=master)](https://coveralls.io/github/linsamtw/FinMind?branch=master)-->


You can analyze financial data without having to collect the data by yourself. The datasets are automatically updated daily.

     pip3 install FinMind
     
 ---------------------
 The full version of this documentation is at [https://linsamtw.github.io/FinMindDoc/](https://linsamtw.github.io/FinMindDoc/).
 
 Financial Visualize [http://finmind.servebeer.com/](http://finmind.servebeer.com/) (In development)
 
 [40 data sets](https://github.com/linsamtw/FinMind/blob/master/dataset.md)

  ----------------------
 #### FinMind 1.0.61 (2019-06-10) 
* Add `Mind`, it can load all information about the Taiwan Stock, <br>
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

		_2330.StockPrice['move_average'] = Mind.MoveAverage(_2330.StockPrice,days = 5,variable = 'close')
		_2330.StockPrice['RSV'] = Mind.RSV(_2330.StockPrice,days = 5)
		_2330.StockPrice['BIAS'] = Mind.BIAS(_2330.StockPrice,days = 5)

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
 ## Load example

### FinMind.Data.Load.transpose(data)
    from FinMind.Data import Load

    TaiwanStockFinancialStatements = Load.FinData(dataset = 'FinancialStatements',select = '2330',date = '2018-01-01')
    print( TaiwanStockFinancialStatements[:5] )
    # transpose
    data = Load.transpose(TaiwanStockFinancialStatements)

### `Balance Sheet` Taiwan 資產負債表
	from FinMind.Data import Load
	data = Load.FinData(dataset = 'BalanceSheet',select = ['2330'],date = '2018-01-10')
	# or 
	from FinMind.Data.Load import BalanceSheet
	data = BalanceSheet(select = ['2330'],date = '2018-01-10')
### `Taiwan Stock Holding SharesPer` Taiwan 股權分散表
	from FinMind.Data import Load
	data = Load.FinData(dataset = 'TaiwanStockHoldingSharesPer',select = ['2330'],date = '2018-10-10')
	# or 
	from FinMind.Data.Load import TaiwanStockHoldingSharesPer
	data = TaiwanStockHoldingSharesPer(select = ['2330'],date = '2018-10-10')
	
### `Taiwan Stock Shareholding` Taiwan 外資持股
	from FinMind.Data import Load
	data = Load.FinData(dataset = 'Shareholding',select = ['2330'],date = '2018-10-10')
	# or 
	from FinMind.Data.Load import Shareholding
	data = Shareholding(select = ['2330'],date = '2018-10-10')
### `Raw Material Futures Prices` 美國原物料期貨 ( meats,grains,energies,softs,metals )
	from FinMind.Data import Load
	RawMaterialFuturesPrices_list = Load.FinDataList(dataset = 'RawMaterialFuturesPrices')
	data = Load.FinData(dataset = 'RawMaterialFuturesPrices',select = [RawMaterialFuturesPrices_list[3]],date = '2018-10-10')
 
 ----------------------
 ### `Taiwan Stock Info` Taiwan 股票資訊, `stock_id` 對應以下 `select`
 	from FinMind.Data import Load
	TaiwanStockInfo = Load.FinData(dataset = 'TaiwanStockInfo')
    
 ### `Taiwan Stock Price` Taiwan 股價
 
 	from FinMind.Data import Load
	TaiwanStockInfo = Load.FinData(dataset = 'TaiwanStockInfo')
	data = Load.FinData(dataset = 'TaiwanStockPrice',select = TaiwanStockInfo.loc[1000,'stock_id'],date = '2018-10-10')
	print( data[:5] )

	    	Open   High    Low  Close  Adj_Close    Volume        date stock_id
        0  233.5  233.5  227.0  227.5      227.5  94589657  2018-10-11     2330
        1  231.0  237.0  229.0  237.0      237.0  47175769  2018-10-12     2330
        2  234.0  234.0  230.5  230.5      230.5  42168280  2018-10-15     2330
        3  229.5  237.0  229.0  237.0      237.0  37818077  2018-10-16     2330
        4  241.5  243.0  238.0  238.5      238.5  42494858  2018-10-17     2330
	
 ### `Taiwan Stock Financial Statements ` Taiwan 股票財報
	from FinMind.Data import Load
	TaiwanStockInfo = Load.FinData(dataset = 'TaiwanStockInfo')
	data = Load.FinData(dataset = 'FinancialStatements',select = TaiwanStockInfo.loc[1000,'stock_id'],date = '2017-10-10')

 ### `Taiwan Stock Stock Dividend ` Taiwan 股票歷年配息
	from FinMind.Data import Load
	TaiwanStockInfo = Load.FinData(dataset = 'TaiwanStockInfo')
	data = Load.FinData(dataset = 'TaiwanStockStockDividend',select = TaiwanStockInfo.loc[1000,'stock_id'],date = '2017-10-10')

 ### `Taiwan Stock Margin Purchase Short Sale ` Taiwan 股票融資融券
	from FinMind.Data import Load
	TaiwanStockInfo = Load.FinData(dataset = 'TaiwanStockInfo')
	data = Load.FinData(dataset = 'TaiwanStockMarginPurchaseShortSale',select = TaiwanStockInfo.loc[1000,'stock_id'],date = '2018-10-10')

 ### `Institutional Investors Buy Sell ` Taiwan 股票外資買賣
 	from FinMind.Data import Load
	TaiwanStockInfo = Load.FinData(dataset = 'TaiwanStockInfo')
	data = Load.FinData(dataset = 'InstitutionalInvestorsBuySell',select = TaiwanStockInfo.loc[1000,'stock_id'],date = '2018-10-10')

 ### `Exchange Rate` 各國匯率
 	from FinMind.Data import Load
	ExchangeRate_list = Load.FinDataList(dataset = 'ExchangeRate')
	data = Load.FinData(dataset = 'ExchangeRate',select = ExchangeRate_list[0],date = '2018-10-10')

 ### `Interest Rate` 各國央行利率
 	from FinMind.Data import Load
	InterestRate_list = Load.FinDataList(dataset = 'InterestRate')
	data = Load.FinData(dataset = 'InterestRate',select = InterestRate_list[0],date = '2018-10-10')

  ### `Government bond` 各國債券
	from FinMind.Data import Load
	GovernmentBonds_list = Load.FinDataList(dataset = 'GovernmentBonds')
	data = Load.FinData(dataset = 'GovernmentBonds',select = GovernmentBonds_list[0],date = '2018-10-10')

 ### `Gold Price` 金價
	from FinMind.Data import Load
	data = Load.FinData(dataset = 'GoldPrice',date = '2018-10-10')    

 ### `Crude Oil Prices` 油價
	from FinMind.Data import Load
	CrudeOilPrices_list = Load.FinDataList(dataset = 'CrudeOilPrices')
	data = Load.FinData(dataset = 'CrudeOilPrices',select = CrudeOilPrices_list[0],date = '2018-10-10')

For other examples, please refer to [demo](https://github.com/linsamtw/FinMind/blob/master/demo.py).

-------------------------------
### Financial Data

[DataSource](https://github.com/linsamtw/FinMind/blob/master/Data/DataSource.md)

* <b>Stock Information</b> `Taiwan`,`US`,`Japan`,`UK`,`Europe`
* <b>Stock Prices</b> `Taiwan`,`US`,`Japan`,`UK`,`Europe`
* <b>Financial Statements </b> `Taiwan`,`US`
* <b>Crude Oil Prices</b> `Brent`,`WTI`
* <b>Exchange Rates ( vs US )</b> `Canada`,`China`,`Euro`,`Japan`,`Taiwan`,`UK`
* <b>Interest Rate</b> `BCB`,`BOC`,`BOE`,`BOJ`,`CBR`,`ECB`,`FED`,`PBOC`,`PBOC`,`RBI`,`RBA`,`RBNZ`,`SNB`
* <b>Government Bonds</b> `Canada`,`China`,`France`,`Germany`,`Italy`,`Japan`,`Russia`,`United Kingdom`,`United States`
* <b>Energy Futures Prices</b> `BrentOilFutures`,`CarbonEmissionsFutures`,`CrudeOilWTIFutures`,`GasolineRBOBFutures`,`HeatingOilFutures`,`LondonGasOilFutures`,`NaturalGasFutures`,
* <b>Raw Material Futures Prices</b> `meats`, `grains`, `energies`, `softs`, `metals`
* <b>Taiwan Stock Stock Dividend</b>
* <b>Taiwan Stock Balance Sheet</b>
* <b>Taiwan Stock Holding Shares Per </b>
* <b>Taiwan Stock Shareholding</b>
* <b>Taiwan Stock Institutional Investors Buy and Sell </b>
* <b>Taiwan Stock Margin Purchase Short Sale</b>
* <b>Taiwan Stock Month Revenue</b>
* <b>Gold Price</b>

### Financial Visualize ( In development )
At least five kinds of visualization tools for every data type. ( In development )<br>
[http://finmind.servebeer.com/](http://finmind.servebeer.com/)
開發中

### Financial Mining ( In development )

[LSTM & GRU](https://github.com/linsamtw/FinMind/tree/master/Mining)

------------------------------------------------------------

email : linsam.tw.github@gmail.com


