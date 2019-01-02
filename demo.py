

from FinMind.Data import Load
#---------------------------------------------------------------

data = Load.FinData(table = 'StockInfo',select = [],date = '')
#---------------------------------------------------------------
data = Load.FinDataList(table = 'StockPrice')
print( data[:5] )
data = Load.FinData(table = 'StockPrice',
                 select = ['2330'],date = '2018-10-10')
print( data[:5] )

#---------------------------------------------------------------
data = Load.FinDataList(table = 'FinancialStatements')
print( data[:5] )
data = Load.FinData(table = 'FinancialStatements',
                 select = ['2330'],date = '2017-10-10')
print( data[:5] )

#---------------------------------------------------------------
data = Load.FinDataList(table = 'StockDividend')
print( data[:5] )
data = Load.FinData(table = 'StockDividend',
                 select = ['2330'],date = '2017-10-10')
print( data[:5] )

#---------------------------------------------------------------
data = Load.FinDataList(table = 'ExchangeRate')
print( data[:5] )
data = Load.FinData(table = 'ExchangeRate',
                 select = ['JPY'],date = '2018-10-10')
print( data[:5] )

#---------------------------------------------------------------
data = Load.FinDataList(table = 'InstitutionalInvestors',
                 date = '2018-10-10')
print( data[:5] )

#---------------------------------------------------------------
data = Load.FinDataList(table = 'InterestRate')
print( data[:5] )
data = Load.FinData(table = 'InterestRate',
                 select = ['BCB'],date = '2018-10-10')
print( data[:5] )

#---------------------------------------------------------------
data = Load.FinDataList(table = 'GovernmentBonds')
print( data[:5] )
data = Load.FinData(table = 'GovernmentBonds',
                 select = ['Canada 1-Month'],date = '2018-10-10')
print( data[:5] )

#---------------------------------------------------------------
data = Load.FinDataList(table = 'CrudeOilPrices')
print( data[:5] )
data = Load.FinData(table = 'CrudeOilPrices',
                 select = ['Brent'],date = '2018-10-10')
print( data[:5] )

#---------------------------------------------------------------
data = Load.FinDataList(table = 'EnergyFuturesPrices')
print( data[:5] )
data = Load.FinData(table = 'EnergyFuturesPrices',
                 select = ['Brent Oil Futures'],date = '2018-10-10')
print( data[:5] )









