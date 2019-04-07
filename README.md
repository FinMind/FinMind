[![Build Status](https://travis-ci.org/linsamtw/FinMind.svg?branch=master)](https://travis-ci.org/linsamtw/FinMind)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/linsamtw/FinMind/blob/master/LICENSE)
[![PyPI version](https://badge.fury.io/py/FinMind.svg)](https://badge.fury.io/py/FinMind)
[![Documentation Status](https://readthedocs.org/projects/finminddoc/badge/?version=latest)](https://finminddoc.readthedocs.io/en/latest/?badge=latest)
<!--[![Coverage Status](https://coveralls.io/repos/github/linsamtw/FinMind/badge.svg?branch=master)](https://coveralls.io/github/linsamtw/FinMind?branch=master)-->


You can analyze financial data without having to collect the data by yourself. The datasets are automatically updated daily.

     pip3 install FinMind
     
 ---------------------
 The full version of this documentation is at [https://linsamtw.github.io/FinMindDoc/](https://linsamtw.github.io/FinMindDoc/).
 
 ----------------------
 #### FinMind 1.0.53 (2019-04-07) 
 ##### Fix FinMind.Data.Load
 * optimize speeds of loading data , ex :
 
		from FinMind.Data import Load
		import datetime

		TaiwanStockInfo = Load.FinData(dataset = 'TaiwanStockInfo')
		s = datetime.datetime.now()
		TaiwanStockFinancialStatements = Load.FinData(
			dataset = 'FinancialStatements',
			select = list(TaiwanStockInfo['stock_id']),
			date = '2018-12-01')
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
 ----------------------
 ## Load example

#### New
### FinMind.Data.Load.transpose(data)
    from FinMind.Data import Load

    TaiwanStockFinancialStatements = Load.FinData(
            dataset = 'FinancialStatements',
            select = '2330.TW',
            date = '2018-01-01')
    print( TaiwanStockFinancialStatements[:5] )
    # transpose
    data = Load.transpose(TaiwanStockFinancialStatements)


### `Balance Sheet` Taiwan 資產負債表

	data = Load.FinData(dataset = 'BalanceSheet',select = ['2330.TW'],date = '2018-01-10')
    
### `Taiwan Stock Holding SharesPer` Taiwan 股權分散表

	data = Load.FinData(dataset = 'TaiwanStockHoldingSharesPer',select = ['2330.TW'],date = '2018-10-10')
    
### `Taiwan Stock Shareholding` Taiwan 外資持股

	data = Load.FinData(dataset = 'Shareholding',select = ['2330.TW'],date = '2018-10-10')
    
### `Raw Material Futures Prices` 美國原物料期貨 ( meats,grains,energies,softs,metals )
	RawMaterialFuturesPrices_list = Load.FinDataList(dataset = 'RawMaterialFuturesPrices')
	data = Load.FinData(dataset = 'RawMaterialFuturesPrices',select = [RawMaterialFuturesPrices_list[3]],date = '2018-10-10')
 
 ----------------------
 ### `Taiwan Stock Info` Taiwan 股票資訊, `stock_id` 對應以下 `select`
 	from FinMind.Data import Load
	TaiwanStockInfo = Load.FinData(dataset = 'TaiwanStockInfo')
    
 ### `Taiwan Stock Price` Taiwan 股價
 
 	from FinMind.Data import Load
	data = Load.FinData(dataset = 'TaiwanStockPrice',select = ['2330.TW'],date = '2018-10-10')
	print( data[:5] )

	    	Open   High    Low  Close  Adj_Close    Volume        date stock_id
        0  233.5  233.5  227.0  227.5      227.5  94589657  2018-10-11     2330.TW
        1  231.0  237.0  229.0  237.0      237.0  47175769  2018-10-12     2330.TW
        2  234.0  234.0  230.5  230.5      230.5  42168280  2018-10-15     2330.TW
        3  229.5  237.0  229.0  237.0      237.0  37818077  2018-10-16     2330.TW
        4  241.5  243.0  238.0  238.5      238.5  42494858  2018-10-17     2330.TW
	
 ### `Taiwan Stock Financial Statements ` Taiwan 股票財報

	data = Load.FinData(dataset = 'FinancialStatements',select = ['2330.TW'],date = '2017-10-10')

 ### `Taiwan Stock Stock Dividend ` Taiwan 股票歷年配息

	data = Load.FinData(dataset = 'TaiwanStockStockDividend',select = ['2330.TW'],date = '2017-10-10')

 ### `Taiwan Stock Margin Purchase Short Sale ` Taiwan 股票融資融券

	data = Load.FinData(dataset = 'TaiwanStockMarginPurchaseShortSale',select = ['2330.TW'],date = '2018-10-10')

 ### `Institutional Investors Buy Sell ` Taiwan 股票外資買賣
 
	data = Load.FinData(dataset = 'InstitutionalInvestorsBuySell',select = ['2330.TW'],date = '2018-10-10')

 ### `Exchange Rate` 各國匯率
 
	data = Load.FinData(dataset = 'ExchangeRate',select = ['Japan'],date = '2018-10-10')

 ### `Interest Rate` 各國央行利率
 
	data = Load.FinData(dataset = 'InterestRate',select = ['ECB'],date = '2018-10-10')

  ### `Government bond` 各國債券

	data = Load.FinData(dataset = 'Governmentbond',select = ['Canada 2-Month'],date = '2018-10-10')

 ### `Gold Price` 金價

	data = Load.FinData(dataset = 'GoldPrice',date = '2018-10-10')    

 ### `Crude Oil Prices` 油價

	data = Load.FinData(dataset = 'CrudeOilPrices',select = ['Brent'],date = '2018-10-10')

For other examples, please refer to [demo](https://github.com/linsamtw/FinMind/blob/master/demo.py).

-------------------------------
### Financial Data
More than 15 kinds of financial data.

* <b>Stock Information</b>
    * Taiwan
    * US
    * Japan
    * UK
    * Europe
* <b>Stock Prices</b>
    * Taiwan
    * US
    * Japan
    * UK
    * Europe
* <b>Financial Statements </b>
    * Taiwan
    * US
* <b>Crude Oil Prices</b>
    * Brent
    * WTI
* <b>Exchange Rates ( vs US )</b>
    * Canada
    * China
    * Euro
    * Japan
    * Taiwan
    * UK
* <b>Interest Rate</b>
    * BCB : Central Bank of Brazil
    * BOC : Bank of Canada
    * BOE : Bank of England
    * BOJ : Bank of Japan
    * CBR : Central Bank of the Russian Federation
    * ECB : European Central Bank
    * FED : Federal Reserve
    * PBOC : People's Bank of China
    * RBA : Reserve Bank of Australia
    * RBI : Reserve Bank of India
    * RBNZ : Reserve Bank of New Zealand
    * SNB :  Swiss National Bank
* <b>Government Bonds</b>
    * Canada : 1-Month ~ 30-Year
    * China : 1-Year ~ 30-Year
    * France : 1-Month ~ 50-Year
    * Germany : 3-Month ~ 30-Year
    * Italy : 1-Month ~ 50-Year
    * Japan : 1-Month ~ 40-Year
    * Russia : 1-Week ~ 20-Year
    * United Kingdom : 1-Month ~ 50-Year
    * United States : 1-Month ~ 30-Year
* <b>Energy Futures Prices</b>
    * BrentOilFutures
    * CarbonEmissionsFutures
    * CrudeOilWTIFutures
    * GasolineRBOBFutures
    * HeatingOilFutures
    * LondonGasOilFutures
    * NaturalGasFutures
* <b>Raw Material Futures Prices ( meats, grains, energies, softs, metals)</b>
* <b>Taiwan Stock Stock Dividend</b>
* <b>Taiwan Stock Balance Sheet</b>
* <b>Taiwan Stock Holding Shares Per </b>
* <b>Taiwan Stock Shareholding</b>
* <b>Taiwan Stock Institutional Investors Buy and Sell </b>
* <b>Taiwan Stock Margin Purchase Short Sale</b>
* <b>Gold Price</b>

### Financial Visualize ( In development )
At least five kinds of visualization tools for every data type. ( In development )<br>
[股價、交易量、金價、油價](http://139.162.122.184:5050/)

### Financial Mining ( In development )

[LSTM & GRU](https://github.com/linsamtw/FinMind/tree/master/Mining)

------------------------------------------------------------

email : linsam.tw.github@gmail.com


