


from FinMind.Mining import Mind

_2330 = Mind.Stock('2330','2019-01-01')

_2330.StockPrice.head()
_2330.FinancialStatements.head()
_2330.ShareHolding.head()
_2330.InstitutionalInvestors.head()
_2330.MarginPurchaseShortSale.head()
_2330.MonthRevenue.head()
_2330.HoldingSharesPer.head()
_2330.BalanceSheet.head()

_2330.StockPrice['move_average'] = Mind.MoveAverage(
        _2330.StockPrice,days = 5,variable = 'close')

_2330.StockPrice['RSV'] = Mind.RSV(
        _2330.StockPrice,days = 5)

_2330.StockPrice['BIAS'] = Mind.BIAS(
        _2330.StockPrice,days = 5)
_2330.StockPrice.head()



