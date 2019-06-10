
## FinMind.Mind

### `Mind`
it can load all information about the Taiwan Stock, [demo](https://github.com/linsamtw/FinMind/blob/master/Mining/demo.py)

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

### `Mind.MoveAverage`
		
	Mind.MoveAverage(_2330.StockPrice,days = 5,variable = 'close')
		
### `Mind.RSV`
	
	Mind.RSV(_2330.StockPrice,days = 5)
	
### `Mind.BIAS`
	
	Mind.BIAS(_2330.StockPrice,days = 5)

--------------------------




## stock price predicting by building GRU & LSTM model.( predict tomorrow stock price )

[demo](https://github.com/linsamtw/FinMind/blob/master/Mining/GRU_LSTM_demo.py)

![pred vs actual](https://github.com/linsamtw/FinMind/blob/master/Mining/GRE_LSTM.png)
