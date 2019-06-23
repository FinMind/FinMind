[![Build Status](https://travis-ci.org/linsamtw/FinMind.svg?branch=master)](https://travis-ci.org/linsamtw/FinMind)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/linsamtw/FinMind/blob/master/LICENSE)
[![PyPI version](https://badge.fury.io/py/FinMind.svg)](https://badge.fury.io/py/FinMind)
[![Documentation Status](https://readthedocs.org/projects/finminddoc/badge/?version=latest)](https://finminddoc.readthedocs.io/en/latest/?badge=latest)
<!--[![Coverage Status](https://coveralls.io/repos/github/linsamtw/FinMind/badge.svg?branch=master)](https://coveralls.io/github/linsamtw/FinMind?branch=master)-->

Solicit partners who are interested in joint development. <br>
徵求有興趣共同開發的夥伴。<br>

## What is it?
**FinMind** is open source of more than 40 dataset, contain Taiwan stock, US stock, Europe stock, Japan stock, oil price, gold price, G7 exchange rate, interest rate, government bonds. The datasets are automatically updated daily.

You can analyze financial data without having to collect the data by yourself. 

     pip3 install FinMind
     
  
  ## Api
  	url = 'http://finmindapi.servebeer.com/api/data'
    form_data = {'dataset':'TaiwanStockInfo'}
    res = requests.post(url,verify = True,data = form_data)

  	url = 'http://finmindapi.servebeer.com/api/data'
    form_data = {'dataset':'TaiwanStockPrice','stock_id':['2330','2317'],'date':'2019-06-01'}
    res = requests.post(url,verify = True,,data = form_data)


  * [python demo](https://github.com/linsamtw/FinMind/blob/master/example/api_demo.py)
  * [R demo](https://github.com/linsamtw/FinMind/blob/master/example/api_demo.r)
  
  ## Data
  	from FinMind.Data import Load
	TaiwanStockInfo = Load.FinData(dataset = 'TaiwanStockInfo')
    data = Load.FinData(dataset = 'TaiwanStockPrice',select = ['2330','2317'],
    					date = '2018-10-10')

  * [FinMind.Data](https://github.com/linsamtw/FinMind/tree/master/Data)
  * [40 data sets](https://github.com/linsamtw/FinMind/blob/master/dataset.md)
  
  ## Mind
  * [FinMind.Mind](https://github.com/linsamtw/FinMind/tree/master/Mining)
  * [GRU_LSTM_demo](https://github.com/linsamtw/FinMind/blob/master/Mining/GRU_LSTM_demo.py)

  ## Document
  * The full version of this documentation is at [https://linsamtw.github.io/FinMindDoc/](https://linsamtw.github.io/FinMindDoc/).
  * [median](https://medium.com/@yanweiliu/finmind-%E4%BD%BF%E7%94%A8python%E6%9F%A5%E5%85%A8%E7%90%83%E8%82%A1%E5%83%B9-%E5%82%B5%E5%88%B8-%E5%8E%9F%E6%B2%B9%E5%83%B9%E6%A0%BC-f39d13ad6a68)


[HistoryUpdate](https://github.com/linsamtw/FinMind/blob/master/HistoryUpdate.md)


### Financial Visualize ( In development )
At least five kinds of visualization tools for every data type. ( In development )<br>
[http://finmind.servebeer.com/](http://finmind.servebeer.com/)
開發中

### [License](https://github.com/linsamtw/FinMind/blob/master/LICENSE)


email : linsam.tw.github@gmail.com


