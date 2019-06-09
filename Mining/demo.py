


from FinMind.Mining import Mind

_2330 = Mind.Stock('2330','2019-01-01')

_2330.StockPrice
_2330.FinancialStatements
_2330.ShareHolding
_2330.InstitutionalInvestors
_2330.MarginPurchaseShortSale
_2330.MonthRevenue
_2330.HoldingSharesPer
_2330.BalanceSheet

_2330.StockPrice['move_average'] = Mind.MoveAverage(
        _2330.StockPrice,days = 5,variable = 'close')


_2330.StockPrice['RSV'] = Mind.RSV(
        _2330.StockPrice,days = 5)

_2330.StockPrice['BIAS'] = Mind.BIAS(
        _2330.StockPrice,days = 5)




