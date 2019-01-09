
### Load Taiwan Stock information
      from FinMind.OpenData.Load import Load

      database = 'TaiwanStockInfo'

      datalist = Load(database = database, datalist = True)
      data = Load( database = database, select = datalist[0] )
      data = Load( database = database, [datalist[0],datalist[1]])
      data = Load(database = database, load_all = True)
        
<html>
<p align="right">
  <a href = 'https://github.com/f496328mm/FinMind/tree/master/OpenData#load-example'> Home </a></p>
</html>   
      
-----------------------------------------------------------------
### Load Taiwan Stock Price
        from FinMind.OpenData.Load import Load

        database = 'StockPrice'

        datalist = Load(database = database,datalist = True)# get stock list
        data_2002 = Load(database = database, select = '2002') # select stock 2002
        mulit_data = Load(database = database, select = ['2002','2330'])# select mulit stock
        all_data = Load(database = database, load_all = True)# select all stock
        
<html>
<p align="right">
  <a href = 'https://github.com/f496328mm/FinMind/tree/master/OpenData#load-example'> Home </a></p>
</html>   

-----------------------------------------------------------------
### Load Taiwan Stock FinancialStatements
        from FinMind.OpenData.Load import Load

        database = 'FinancialStatements'
        datalist = Load(database = database,datalist = True)# get stock list
        data = Load(database = database, select = '2002') # select stock 2002
        data = Load(database = database, select = ['2002','2330'])# select mulit stock
        data = Load(database = database, load_all = True)# select all stock
        
<html>
<p align="right">
  <a href = 'https://github.com/f496328mm/FinMind/tree/master/OpenData#load-example'> Home </a></p>
</html>   
      
-----------------------------------------------------------------
### Load Taiwan Stock StockDividend

      from FinMind.OpenData.Load import Load

      database = 'StockDividend'
      datalist = Load(database = database,datalist = True)# get stock list
      data = Load(database = database, select = '2002') # select stock 2002
      data = Load(database = database, select = ['2002','2330'])# select mulit stock
      data = Load(database = database, load_all = True)# select all stock
        
<html>
<p align="right">
  <a href = 'https://github.com/f496328mm/FinMind/tree/master/OpenData#load-example'> Home </a></p>
</html>   
      
-----------------------------------------------------------------
### Load Taiwan Stock InstitutionalInvestors buy and sell
        from FinMind.OpenData.Load import Load

        database = 'InstitutionalInvestors'
        data = Load(database = database) 
        
<html>
<p align="right">
  <a href = 'https://github.com/f496328mm/FinMind/tree/master/OpenData#load-example'> Home </a></p>
</html>   
              
-----------------------------------------------------------------
### Load CrudeOilPrices
        from FinMind.OpenData.Load import Load

        database = 'CrudeOilPrices'
        data = Load(database = database)
        
<html>
<p align="right">
  <a href = 'https://github.com/f496328mm/FinMind/tree/master/OpenData#load-example'> Home </a></p>
</html>   
              
-----------------------------------------------------------------
### Load ExchangeRate
        from FinMind.OpenData.Load import Load

        database = 'ExchangeRate'
        datalist = Load(database = database,datalist = True)# get country list
        data = Load(database = database, select = 'GBP') # select country GBP
        data = Load(database = database, select = ['GBP','HKD'])# select mulit country
        data = Load(database = database, load_all = True)# select all stock
        
<html>
<p align="right">
  <a href = 'https://github.com/f496328mm/FinMind/tree/master/OpenData#load-example'> Home </a></p>
</html>   
              
-----------------------------------------------------------------
### Load Central Band InterestRate
        from FinMind.OpenData.Load import Load

        database = 'InterestRate'
        datalist = Load(database = database,datalist = True)# get country list
        data = Load(database = database, select = 'FED')# select country FED
        data = Load(database = database, select = ['FED','ECB'])# select mulit country
        data = Load(database = database, load_all = True)# select all stock
        
<html>
<p align="right">
  <a href = 'https://github.com/f496328mm/FinMind/tree/master/OpenData#load-example'> Home </a></p>
</html>   
              
-----------------------------------------------------------------
### Load Gold Price
        from FinMind.OpenData.Load import Load

        database = 'GoldPrice'
        data = Load(database = database)
        
<html>
<p align="right">
  <a href = 'https://github.com/f496328mm/FinMind/tree/master/OpenData#load-example'> Home </a></p>
</html>   

-----------------------------------------------------------------
### Load Government Bonds
        from FinMind.OpenData.Load import Load

        database = 'GovernmentBonds'
        datalist = Load(database = database,datalist = True)# get GovernmentBonds list
        data = Load(database = database, select = datalist[0]) # select GovernmentBonds 0
        data = Load(database = database, select = [datalist[0],datalist[1]])# select mulit GovernmentBonds
        data = Load(database = database, load_all = True)# select all GovernmentBonds
        
<html>
<p align="right">
  <a href = 'https://github.com/f496328mm/FinMind/tree/master/OpenData#load-example'> Home </a></p>
</html>    

-----------------------------------------------------------------
### Load Energy Futures Prices
        from FinMind.OpenData.Load import Load

        database = 'EnergyFuturesPrices'
        datalist = Load(database = database,datalist = True)# get EnergyFuturesPrices list
        data = Load(database = database, select = datalist[0]) # select EnergyFuturesPrices 0
        data = Load(database = database, select = [datalist[0],datalist[1]])# select mulit EnergyFuturesPrices
        data = Load(database = database, load_all = True)# select all EnergyFuturesPrices
        
<html>
<p align="right">
  <a href = 'https://github.com/f496328mm/FinMind/tree/master/OpenData#load-example'> Home </a></p>
</html>   
              
-----------------------------------------------------------------
