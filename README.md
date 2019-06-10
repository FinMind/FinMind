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

### Financial Visualize ( In development )
At least five kinds of visualization tools for every data type. ( In development )<br>
[http://finmind.servebeer.com/](http://finmind.servebeer.com/)
開發中

------------------------------------------------------------
### [License](https://github.com/linsamtw/FinMind/blob/master/LICENSE)


email : linsam.tw.github@gmail.com


