[![Build Status](https://travis-ci.org/linsamtw/FinMind.svg?branch=master)](https://travis-ci.org/linsamtw/FinMind)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/linsamtw/FinMind/blob/master/LICENSE)
[![PyPI version](https://badge.fury.io/py/FinMind.svg)](https://badge.fury.io/py/FinMind)
[![Documentation Status](https://readthedocs.org/projects/finminddoc/badge/?version=latest)](https://finminddoc.readthedocs.io/en/latest/?badge=latest)
<!--[![Coverage Status](https://coveralls.io/repos/github/linsamtw/FinMind/badge.svg?branch=master)](https://coveralls.io/github/linsamtw/FinMind?branch=master)-->


You can analysis financial data and no need collecting data by yourself. The dataset will auto update daily.

     pip3 install FinMind
     
 ---------------------
 The full version of this documentation is at https://linsamtw.github.io/FinMindDoc/.
 
 #### example
 Load Taiwan stock price 2330 starting at 2018-10-10.
 
    >>> from FinMind.Data import Load
	>>> data = Load.FinData(dataset = 'TaiwanStockPrice',select = ['2330.TW'],date = '2018-10-10')
	>>> print( data[:5] )

	    	Open   High    Low  Close  Adj_Close    Volume        date stock_id
        0  233.5  233.5  227.0  227.5      227.5  94589657  2018-10-11     2330.TW
        1  231.0  237.0  229.0  237.0      237.0  47175769  2018-10-12     2330.TW
        2  234.0  234.0  230.5  230.5      230.5  42168280  2018-10-15     2330.TW
        3  229.5  237.0  229.0  237.0      237.0  37818077  2018-10-16     2330.TW
        4  241.5  243.0  238.0  238.5      238.5  42494858  2018-10-17     2330.TW
	
other example can refer [demo](https://github.com/linsamtw/FinMind/blob/master/demo.py).

-------------------------------
### Financial Data
More than 15 kinds financial data.

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
* <b>Exchange Rate ( vs US )</b>
    * Canda
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
* <b>Government bond</b>
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
* <b>Taiwan Stock Stock Dividend</b>
* <b>Taiwan Stock Institutional Investors Buy and Sell </b>
* <b>Taiwan Stock Margin Purchase Short Sale</b>
* <b>Gold Price</b>
     
### Financial Visualize
At least five kinds Visualize tools on every data. ( In development )<br>
[股價、交易量、金價、油價](http://139.162.122.184:5050/)

### Financial Mining
Holistic financial analysis. ( In development )

------------------------------------------------------------

email : linsam.tw.github@gmail.com


