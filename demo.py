

import sys
sys.path.append('/home/sam/project/github')
from financialmining.API import Load
#---------------------------------------------------------------

data = Load.Load(table = 'StockInfo',select = [],date = '')
#---------------------------------------------------------------
data = Load.LoadTableList(table = 'StockPrice')
print( data[:5] )
data = Load.Load(table = 'StockPrice',
                 select = ['2330'],date = '2018-10-10')
print( data[:5] )

#---------------------------------------------------------------
data = Load.LoadTableList(table = 'FinancialStatements')
print( data[:5] )
data = Load.Load(table = 'FinancialStatements',
                 select = ['2330'],date = '2018-10-10')
print( data[:5] )

#---------------------------------------------------------------
data = Load.LoadTableList(table = 'StockDividend')
print( data[:5] )
data = Load.Load(table = 'StockDividend',
                 select = ['2330'],date = '2018-10-10')
print( data[:5] )

#---------------------------------------------------------------
data = Load.LoadTableList(table = 'ExchangeRate')
print( data[:5] )
data = Load.Load(table = 'ExchangeRate',
                 select = ['JPY'],date = '2018-10-10')
print( data[:5] )

#---------------------------------------------------------------
data = Load.Load(table = 'InstitutionalInvestors',
                 date = '2018-10-10')
print( data[:5] )

#---------------------------------------------------------------
data = Load.LoadTableList(table = 'InterestRate')
print( data[:5] )
data = Load.Load(table = 'InterestRate',
                 select = ['BCB'],date = '2018-10-10')
print( data[:5] )

#---------------------------------------------------------------
data = Load.LoadTableList(table = 'GovernmentBonds')
print( data[:5] )
data = Load.Load(table = 'GovernmentBonds',
                 select = ['Canada-1-Month'],date = '2018-10-10')
print( data[:5] )

#---------------------------------------------------------------
data = Load.LoadTableList(table = 'GovernmentBonds')
print( data[:5] )
data = Load.Load(table = 'GovernmentBonds',
                 select = ['Canada 1-Month'],date = '2018-10-10')
print( data[:5] )

#---------------------------------------------------------------
data = Load.LoadTableList(table = 'CrudeOilPrices')
print( data[:5] )
data = Load.Load(table = 'CrudeOilPrices',
                 select = ['Brent'],date = '2018-10-10')
print( data[:5] )

#---------------------------------------------------------------
data = Load.LoadTableList(table = 'EnergyFuturesPrices')
print( data[:5] )
data = Load.Load(table = 'EnergyFuturesPrices',
                 select = ['Brent Oil Futures'],date = '2018-10-10')
print( data[:5] )









