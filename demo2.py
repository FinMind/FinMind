

from FinMind.Data.Load import TaiwanStockInfo,TaiwanStockPrice,FinancialStatements
from FinMind.Data.Load import TaiwanStockStockDividend,TaiwanStockMarginPurchaseShortSale,InstitutionalInvestorsBuySell
from FinMind.Data.Load import Shareholding,BalanceSheet,USStockInfo
from FinMind.Data.Load import USStockPrice,JapanStockInfo,JapanStockPrice
from FinMind.Data.Load import UKStockInfo,UKStockPrice,EuropeStockInfo
from FinMind.Data.Load import EuropeStockPrice,ExchangeRateList,ExchangeRate
from FinMind.Data.Load import InstitutionalInvestorsList,InstitutionalInvestors,InterestRateList
from FinMind.Data.Load import InterestRate,GovernmentBondsList,GovernmentBonds
from FinMind.Data.Load import CrudeOilPricesList,CrudeOilPrices,EnergyFuturesPricesList
from FinMind.Data.Load import EnergyFuturesPrices,GoldPrice,CurrencyCirculationList
from FinMind.Data.Load import CurrencyCirculation,TaiwanStockHoldingSharesPer
from FinMind.Data.Load import TaiwanStockMonthRevenue

import datetime

date = str( datetime.datetime.now().date() - datetime.timedelta(30) )
date2 = str( datetime.datetime.now().date() - datetime.timedelta(200) )
date3 = str( datetime.datetime.now().date() - datetime.timedelta(400) )
#---------------------------------------------------------------
print('load TaiwanStockInfo')
tsi = TaiwanStockInfo()
print( tsi[:5] )
_index = 477

print('load TaiwanStockPrice {} '.format(tsi.loc[_index,'stock_id']))
tsp = TaiwanStockPrice(select = tsi.loc[_index,'stock_id'],date = date)
print( tsp[:5] )

print('load 財報 FinancialStatements {} '.format(tsi.loc[_index,'stock_id']))
tsfs = FinancialStatements(select = tsi.loc[_index,'stock_id'],date = date3)
print( tsfs[:5] )
tsfs = FinancialStatements(select = tsi.loc[_index,'stock_id'],year = 2018,season = 1)
print( tsfs[:5] )

print('load 台股配息 TaiwanStockStockDividend {} '.format(tsi.loc[_index,'stock_id']))
tssd = TaiwanStockStockDividend(select = tsi.loc[_index,'stock_id'],date = date3)
print( tssd[:5] )

print('load 借卷融資 TaiwanStockMarginPurchaseShortSale {} '.format(tsi.loc[_index,'stock_id']))
tsmpss = TaiwanStockMarginPurchaseShortSale(
        select = tsi.loc[_index,'stock_id'],date = date3)
print( tsmpss[:5] )

print('load 外資買賣 InstitutionalInvestorsBuySell {} '.format(tsi.loc[_index,'stock_id']))
iibs = InstitutionalInvestorsBuySell(select = tsi.loc[_index,'stock_id'],date = date3)
print( iibs[:5] )

print('load 外資持股 Shareholding {} '.format(tsi.loc[_index,'stock_id']))
sh = Shareholding(select = tsi.loc[_index,'stock_id'],date = date3)
print( sh[:5] )

print('load 資產負債表 BalanceSheet {} '.format(tsi.loc[_index,'stock_id']))
bs = BalanceSheet(select = tsi.loc[_index,'stock_id'],date = date3)
print( bs[:5] )
bs = BalanceSheet(select = tsi.loc[_index,'stock_id'],year = 2018,season = 1)
print( bs[:5] )

print('load 月營收 TaiwanStockMonthRevenue {} '.format(tsi.loc[_index,'stock_id']))
tsmr = TaiwanStockMonthRevenue(select = tsi.loc[_index,'stock_id'],date = date3)
print( tsmr[:5] )
#---------------------------------------------------------------
print('load USStockInfo')
ussi = USStockInfo()
print( ussi[:5] )

print('load USStockPrice {} '.format(ussi.loc[20,'stock_id']))
ussp = USStockPrice(select = ussi.loc[20,'stock_id'],date = date)
print( ussp[:5] )

print('load 財報 FinancialStatements {} '.format(ussi.loc[20,'stock_id']))
usfs = FinancialStatements(select = ussi.loc[20,'stock_id'],date = date2)
print(usfs)
#---------------------------------------------------------------
print('load JapanStockInfo')
jsi = JapanStockInfo()
print( jsi[:5] )

print('load JapanStockPrice {} '.format(jsi.loc[2,'stock_id']))
jsp = JapanStockPrice(select = jsi.loc[2,'stock_id'],date = date)
print( jsp[:5] )
#---------------------------------------------------------------
print('load UKStockInfo')
uksi = UKStockInfo()
print( uksi[:5] )

print('load UKStockPrice {} '.format(uksi.loc[2,'stock_id']))
uksp = UKStockPrice(select = uksi.loc[2,'stock_id'],date = date)
print( uksp[:5] )
#---------------------------------------------------------------
print('load EuropeStockInfo')
esi = EuropeStockInfo()
print( esi[:5] )

print('load EuropeStockPrice {} '.format(esi.loc[2,'stock_id']))
esp = EuropeStockPrice(select = esi.loc[2,'stock_id'],date = date)
print( esp[:5] )
#---------------------------------------------------------------
print('load ExchangeRate list')
erl = ExchangeRateList()
print( erl[:5] )

print('load ExchangeRate {}'.format(erl[3]))
er = ExchangeRate(select = erl[3],date = date)
print( er[:5] )

#---------------------------------------------------------------
print('load InstitutionalInvestors list')
iil = InstitutionalInvestorsList()
print( iil[:5] )

print('load InstitutionalInvestors {}'.format(iil[3]))
ii = InstitutionalInvestors(select = iil[1],date = date)
print( ii[:5] )

#---------------------------------------------------------------
print('load InterestRate list')
irl = InterestRateList()
print( irl[:5] )

print('load InterestRate {}'.format(irl[3]))
ir = InterestRate(select = irl[5],date = date2)
print( ir[:5] )

#---------------------------------------------------------------
print('load GovernmentBonds list')
gbl = GovernmentBondsList()
print( gbl[:5] )

print('load GovernmentBonds {}'.format(gbl[3]))
GovernmentBonds = GovernmentBonds(select = gbl[3],date = date)
print( GovernmentBonds[:5] )

#---------------------------------------------------------------
print('load CrudeOilPrices list')
copl = CrudeOilPricesList()
print( copl[:5] )

print('load CrudeOilPrices {}'.format(copl[1]))
cop = CrudeOilPrices(select = copl[1],date = date)
print( cop[:5] )

#---------------------------------------------------------------
print('load GoldPrice ')
gp = GoldPrice(date = date)
print( gp[:5] )
#---------------------------------------------------------------
print('load CurrencyCirculation list')
ccl = CurrencyCirculationList()
print( ccl[:5] )

print('load CurrencyCirculation ')
cc = CurrencyCirculation(select = ccl[0],date = '2019-01-04')
print( cc[:5] )

print('load TaiwanStockHoldingSharesPer ')
tshsp = TaiwanStockHoldingSharesPer(select = '2330',date = '2019-01-04')
print( tshsp[:5] )


