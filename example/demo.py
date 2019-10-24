

from FinMind.Data import Load
import datetime

date = str( datetime.datetime.now().date() - datetime.timedelta(30) )
date2 = str( datetime.datetime.now().date() - datetime.timedelta(200) )
date3 = str( datetime.datetime.now().date() - datetime.timedelta(400) )
#---------------------------------------------------------------
print('load TaiwanStockInfo')
TaiwanStockInfo = Load.FinData(dataset = 'TaiwanStockInfo')
print( TaiwanStockInfo[:5] )
_index = 9010

print('load TotalMarginPurchaseShortSale')
TotalMarginPurchaseShortSale = Load.FinData(dataset = 'TotalMarginPurchaseShortSale',
                               date = date)
print( TotalMarginPurchaseShortSale[:5] )

print('load TaiwanStockNews')
TaiwanStockNews = Load.FinData(dataset = 'TaiwanStockNews',
                               date = date,
                               select = '2317')
print( TaiwanStockNews[:5] )

print('load TaiwanStockPrice {} '.format(TaiwanStockInfo.loc[_index,'stock_id']))
TaiwanStockPrice = Load.FinData(
        dataset = 'TaiwanStockPrice',
        select = '2330',
        date = date2 )
print( TaiwanStockPrice[:5] )

print('load 財報 FinancialStatements {} '.format(TaiwanStockInfo.loc[_index,'stock_id']))
TaiwanStockFinancialStatements = Load.FinData(
        dataset = 'FinancialStatements',
        select = TaiwanStockInfo.loc[9010,'stock_id'],
        date = date3)
print( TaiwanStockFinancialStatements[:5] )
# transpose
data = Load.transpose(TaiwanStockFinancialStatements)

print('load 台股配息 TaiwanStockStockDividend {} '.format(TaiwanStockInfo.loc[_index,'stock_id']))
TaiwanStockStockDividend = Load.FinData(
        dataset = 'TaiwanStockStockDividend',
        select = TaiwanStockInfo.loc[_index,'stock_id'],
        date = date3)
print( TaiwanStockStockDividend[:5] )

print('load 台股配息 StockDividend 0050 ')
data = Load.FinData(
        dataset = 'StockDividend',
        select = '0050',
        date = '2015-01-01')
data['date'] = data['date'] + '-' + data['period']
#data = data.drop('period',axis = 1)
data = Load.transpose(data)

print('load 借卷融資 TaiwanStockMarginPurchaseShortSale {} '.format(TaiwanStockInfo.loc[_index,'stock_id']))
TaiwanStockMarginPurchaseShortSale = Load.FinData(
        dataset = 'TaiwanStockMarginPurchaseShortSale',
        select = TaiwanStockInfo.loc[_index,'stock_id'],
        date = date3)
print( TaiwanStockMarginPurchaseShortSale[:5] )

print('load total 借卷融資 TotalMarginPurchaseShortSale ')
TotalMarginPurchaseShortSale = Load.FinData(
        dataset = 'TotalMarginPurchaseShortSale',
        date = date3)
print( TotalMarginPurchaseShortSale[:5] )

print('load 外資買賣 InstitutionalInvestorsBuySell {} '.format(TaiwanStockInfo.loc[_index,'stock_id']))
InstitutionalInvestorsBuySell = Load.FinData(
        dataset = 'InstitutionalInvestorsBuySell',
        select = TaiwanStockInfo.loc[_index,'stock_id'],
        date = date3)
print( InstitutionalInvestorsBuySell[:5] )

print('load 外資持股 Shareholding {} '.format(TaiwanStockInfo.loc[_index,'stock_id']))
Shareholding = Load.FinData(
        dataset = 'Shareholding',
        select = TaiwanStockInfo.loc[_index,'stock_id'],
        date = date3)
print( Shareholding[:5] )

print('load 資產負債表 BalanceSheet {} '.format(TaiwanStockInfo.loc[_index,'stock_id']))
BalanceSheet = Load.FinData(
        dataset = 'BalanceSheet',
        select = '2317',
        date = date3)
print( BalanceSheet[:5] )
data = Load.transpose(BalanceSheet)

print('load 股權分散表 TaiwanStockHoldingSharesPer {} '.format(TaiwanStockInfo.loc[_index,'stock_id']))
TaiwanStockHoldingSharesPer = Load.FinData(
        dataset = 'TaiwanStockHoldingSharesPer',
        select = TaiwanStockInfo.loc[_index,'stock_id'],
        date = date3)
print( TaiwanStockHoldingSharesPer[:5] )

print('load 月營收 TaiwanStockMonthRevenue {} '.format(TaiwanStockInfo.loc[_index,'stock_id']))
TaiwanStockMonthRevenue = Load.FinData(
        dataset = 'TaiwanStockMonthRevenue',
        select = TaiwanStockInfo.loc[_index,'stock_id'],
        date = date3)
print( TaiwanStockMonthRevenue[:5] )


print('load 選擇權 TaiwanOption ')
TaiwanOption = Load.FinData(
        dataset = 'TaiwanOption',
        select = 'OCO',
        date = '2019-09-05',)
print( TaiwanOption[:5] )


print('load 期貨 TaiwanFutures ')
TaiwanFutures = Load.FinData(
        dataset = 'TaiwanFutures',
        select = 'MTX',
        date = '2019-09-02')
print( TaiwanFutures[:5] )

#---------------------------------------------------------------
print('load USStockInfo')
USStockInfo = Load.FinData(dataset = 'USStockInfo')
print( USStockInfo[:5] )

print('load USStockPrice {} '.format(USStockInfo.loc[20,'stock_id']))
USStockPrice = Load.FinData(
        dataset = 'USStockPrice',
        select = USStockInfo.loc[20,'stock_id'],
        date = date)
print( USStockPrice[:5] )

print('load 財報 FinancialStatements {} '.format(USStockInfo.loc[15,'stock_id']))
USStockFinancialStatements = Load.FinData(
        dataset = 'FinancialStatements',
        select = USStockInfo.loc[15,'stock_id'],
        date = date3)
print(USStockFinancialStatements)
#---------------------------------------------------------------
print('load JapanStockInfo')
JapanStockInfo = Load.FinData(dataset = 'JapanStockInfo')
print( JapanStockInfo[:5] )

print('load JapanStockPrice {} '.format(JapanStockInfo.loc[2,'stock_id']))
JapanStockPrice = Load.FinData(
        dataset = 'JapanStockPrice',
        select = JapanStockInfo.loc[2,'stock_id'],
        date = date)
print( JapanStockPrice[:5] )
#---------------------------------------------------------------
print('load UKStockInfo')
UKStockInfo = Load.FinData(dataset = 'UKStockInfo')
print( UKStockInfo[:5] )

print('load UKStockPrice {} '.format(UKStockInfo.loc[2,'stock_id']))
UKStockPrice = Load.FinData(
        dataset = 'UKStockPrice',
        select = UKStockInfo.loc[200,'stock_id'],
        date = date)
print( UKStockPrice[:5] )
#---------------------------------------------------------------
print('load EuropeStockInfo')
EuropeStockInfo = Load.FinData(dataset = 'EuropeStockInfo')
print( EuropeStockInfo[:5] )

print('load EuropeStockPrice {} '.format(EuropeStockInfo.loc[2,'stock_id']))
EuropeStockPrice = Load.FinData(
        dataset = 'EuropeStockPrice',
        select = EuropeStockInfo.loc[2,'stock_id'],
        date = date)
print( EuropeStockPrice[:5] )
#---------------------------------------------------------------
print('load ExchangeRate list')
ExchangeRate_list = Load.FinDataList(dataset = 'ExchangeRate')
print( ExchangeRate_list[:5] )

print('load ExchangeRate {}'.format(ExchangeRate_list[3]))
ExchangeRate = Load.FinData(
        dataset = 'ExchangeRate',
        select = ExchangeRate_list[3],
        date = date)
print( ExchangeRate[:5] )

#---------------------------------------------------------------

print('load InstitutionalInvestors')
InstitutionalInvestors = Load.FinData(
        dataset = 'InstitutionalInvestors',
        date = date)
print( InstitutionalInvestors[:5] )

#---------------------------------------------------------------
print('load InterestRate list')
InterestRate_list = Load.FinDataList(dataset = 'InterestRate')
print( InterestRate_list[:5] )

print('load InterestRate {}'.format(InterestRate_list[3]))
InterestRate = Load.FinData(
        dataset = 'InterestRate',
        select = InterestRate_list[5],
        date = date2)
print( InterestRate[:5] )

#---------------------------------------------------------------
print('load GovernmentBonds list')
GovernmentBonds_list = Load.FinDataList(dataset = 'GovernmentBonds')
print( GovernmentBonds_list[:5] )

print('load GovernmentBonds {}'.format(GovernmentBonds_list[3]))
GovernmentBonds = Load.FinData(
        dataset = 'GovernmentBonds',
        select = GovernmentBonds_list[3],
        date = date)
print( GovernmentBonds[:5] )

#---------------------------------------------------------------
print('load CrudeOilPrices list')
CrudeOilPrices_list = Load.FinDataList(dataset = 'CrudeOilPrices')
print( CrudeOilPrices_list[:5] )

print('load CrudeOilPrices {}'.format(CrudeOilPrices_list[1]))
CrudeOilPrices = Load.FinData(
        dataset = 'CrudeOilPrices',
        select = CrudeOilPrices_list[1],
        date = date)
print( CrudeOilPrices[:5] )

#---------------------------------------------------------------
print('load RawMaterialFuturesPrices list')
RawMaterialFuturesPrices_list = Load.FinDataList(dataset = 'RawMaterialFuturesPrices')
print( RawMaterialFuturesPrices_list[:5] )

print('load RawMaterialFuturesPrices {}'.format(RawMaterialFuturesPrices_list[3]))
RawMaterialFuturesPrices = Load.FinData(
        dataset = 'RawMaterialFuturesPrices',
        select = RawMaterialFuturesPrices_list[3],
        date = date)
print( RawMaterialFuturesPrices[:5] )
#---------------------------------------------------------------
print('load GoldPrice ')
GoldPrice = Load.FinData(
        dataset = 'GoldPrice',
        date = date)
print( GoldPrice[:5] )
#---------------------------------------------------------------
print('load CurrencyCirculation list')
CurrencyCirculation_list = Load.FinDataList(dataset = 'CurrencyCirculation')
print( CurrencyCirculation_list[:5] )

print('load CurrencyCirculation ')
CurrencyCirculation = Load.FinData(
        dataset = 'CurrencyCirculation',
        select = CurrencyCirculation_list[1],
        date = date)
print( CurrencyCirculation[:5] )


