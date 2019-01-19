[![Build Status](https://travis-ci.org/linsamtw/FinMind.svg?branch=master)](https://travis-ci.org/linsamtw/FinMind)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/linsamtw/FinMind/blob/master/LICENSE)
[![PyPI version](https://badge.fury.io/py/FinMind.svg)](https://badge.fury.io/py/FinMind)
[![Documentation Status](https://readthedocs.org/projects/finminddoc/badge/?version=latest)](https://finminddoc.readthedocs.io/en/latest/?badge=latest)
[![Coverage Status](https://coveralls.io/repos/github/linsamtw/FinMind/badge.svg?branch=master)](https://coveralls.io/github/linsamtw/FinMind?branch=master)


You can analysis financial data and no need collecting data by yourself. The dataset will auto update daily.

     pip3 install FinMind
     
 ---------------------
 The full version of this documentation is at https://linsamtw.github.io/FinMindDoc/.
 
 #### example
 Load Taiwan stock price 2330 starting at 2018-10-10.
 
    >>> from FinMind.Data import Load
	>>> data = Load.FinData(dataset = 'StockPrice',select = ['2330'],date = '2018-10-10')
	>>> print( data[:5] )

	    	Open   High    Low  Close  Adj_Close    Volume        date stock_id
        0  233.5  233.5  227.0  227.5      227.5  94589657  2018-10-11     2330
        1  231.0  237.0  229.0  237.0      237.0  47175769  2018-10-12     2330
        2  234.0  234.0  230.5  230.5      230.5  42168280  2018-10-15     2330
        3  229.5  237.0  229.0  237.0      237.0  37818077  2018-10-16     2330
        4  241.5  243.0  238.0  238.5      238.5  42494858  2018-10-17     2330
	
other example can refer [demo](https://github.com/linsamtw/FinMind/blob/master/demo.py).

-------------------------------
### Financial Data
More than ten kinds financial data.

* Stock Information
	* Taiwan
	* US
	* Japan
	* UK
	* Europe
* Stock Prices
	* Taiwan
	* US
	* Japan
	* UK
	* Europe		
* Financial Statements
	* Taiwan
* Stock Dividend
	* Taiwan
* Taiwan Stock Institutional Investors Buy and Sell
* Crude Oil Prices
* Exchange Rate
* Interest Rate
* Gold Price
* Government bond
* Energy Futures Prices
* Gold Price
     
### Financial Visualize
At least five kinds Visualize tools on every data. ( In development )

### Financial Mining
Holistic financial analysis. ( In development )

------------------------------------------------------------

email : linsam.tw.github@gmail.com


