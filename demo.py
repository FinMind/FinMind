

from FinMind.Data import Load
#---------------------------------------------------------------

data = Load.FinData(dataset = 'StockInfo',select = [],date = '')
#---------------------------------------------------------------
data = Load.FinDataList(dataset = 'StockPrice')
print( data[:5] )
data = Load.FinData(dataset = 'StockPrice',
                 select = ['2330'],date = '2018-10-10')
print( data[:5] )

#---------------------------------------------------------------
data = Load.FinDataList(dataset = 'FinancialStatements')
print( data[:5] )
data = Load.FinData(dataset = 'FinancialStatements',
                 select = ['2330'],date = '2017-10-10')
print( data[:5] )

#---------------------------------------------------------------
data = Load.FinDataList(dataset = 'StockDividend')
print( data[:5] )
data = Load.FinData(dataset = 'StockDividend',
                 select = ['2330'],date = '2017-10-10')
print( data[:5] )

#---------------------------------------------------------------
data = Load.FinDataList(dataset = 'ExchangeRate')
print( data[:5] )
data = Load.FinData(dataset = 'ExchangeRate',
                 select = ['JPY'],date = '2018-10-10')
print( data[:5] )

#---------------------------------------------------------------
data = Load.FinData(dataset = 'InstitutionalInvestors',
                 date = '2018-10-10')
print( data[:5] )

#---------------------------------------------------------------
data = Load.FinDataList(dataset = 'InterestRate')
print( data[:5] )
data = Load.FinData(dataset = 'InterestRate',
                 select = ['BCB'],date = '2018-10-10')
print( data[:5] )

#---------------------------------------------------------------
data = Load.FinDataList(dataset = 'GovernmentBonds')
print( data[:5] )
data = Load.FinData(dataset = 'GovernmentBonds',
                 select = ['Canada 1-Month'],date = '2018-10-10')
print( data[:5] )

#---------------------------------------------------------------
data = Load.FinDataList(dataset = 'CrudeOilPrices')
print( data[:5] )
data = Load.FinData(dataset = 'CrudeOilPrices',
                 select = ['Brent'],date = '2018-10-10')
print( data[:5] )

#---------------------------------------------------------------
data = Load.FinDataList(dataset = 'EnergyFuturesPrices')
print( data[:5] )
data = Load.FinData(dataset = 'EnergyFuturesPrices',
                 select = ['Brent Oil Futures'],date = '2018-10-10')
print( data[:5] )









