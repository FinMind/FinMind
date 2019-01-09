

from FinMind.Data import Load
import datetime

date = str( datetime.datetime.now().date() )

#---------------------------------------------------------------
data = Load.FinData(dataset = 'TaiwanStockInfo')
#---------------------------------------------------------------
data = Load.FinDataList(dataset = 'StockPrice')
print( data[:5] )
data = Load.FinData(dataset = 'StockPrice',
                 select = '2330',date = date)
print( data[:5] )

#---------------------------------------------------------------
data = Load.FinDataList(dataset = 'FinancialStatements')
print( data[:5] )
data = Load.FinData(dataset = 'FinancialStatements',
                 select = '2330',date = date)
print( data[:5] )

#---------------------------------------------------------------
data = Load.FinDataList(dataset = 'StockDividend')
print( data[:5] )
data = Load.FinData(dataset = 'StockDividend',
                 select = '2330',date = date)
print( data[:5] )

#---------------------------------------------------------------
data = Load.FinDataList(dataset = 'ExchangeRate')
print( data[:5] )
data = Load.FinData(dataset = 'ExchangeRate',
                 select = 'JPY',date = date)
print( data[:5] )

#---------------------------------------------------------------
data = Load.FinDataList(dataset = 'InstitutionalInvestors')
print( data[:5] )

data = Load.FinData(dataset = 'InstitutionalInvestors',
                 select = 'Dealer',date = date)
print( data[:5] )

#---------------------------------------------------------------
data = Load.FinDataList(dataset = 'InterestRate')
print( data[:5] )
data = Load.FinData(dataset = 'InterestRate',
                 select = 'BCB',date = date)
print( data[:5] )

#---------------------------------------------------------------
data = Load.FinDataList(dataset = 'GovernmentBonds')
print( data[:5] )
data = Load.FinData(dataset = 'GovernmentBonds',
                 select = 'Canada 1-Month',date = date)
print( data[:5] )

#---------------------------------------------------------------
data = Load.FinDataList(dataset = 'CrudeOilPrices')
print( data[:5] )
data = Load.FinData(dataset = 'CrudeOilPrices',
                 select = 'Brent',date = date)
print( data[:5] )

#---------------------------------------------------------------
data = Load.FinDataList(dataset = 'EnergyFuturesPrices')
print( data[:5] )
data = Load.FinData(dataset = 'EnergyFuturesPrices',
                 select = 'Brent Oil Futures',date = date)
print( data[:5] )
#---------------------------------------------------------------
data = Load.FinData(dataset = 'GoldPrice',
                 date = date)
print( data[:5] )








