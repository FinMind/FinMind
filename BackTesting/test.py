

from FinMind.BackTesting import BackTest
import pandas as pd

#------------------------------------------------------------------------------
# example strategy
class demo:
    def __init__(self,
                 stock_price,
                 **kwargs,):
        #-------------------------------------------------------------------    
        # 此區塊請勿更動
        stock_price = stock_price.sort_values('date')
        # 股價
        self.stock_price = stock_price
        # 融資融券
        self.MarginPurchaseShortSale = kwargs.get("MarginPurchaseShortSale", pd.DataFrame())
        # 三大法人買賣
        self.InstitutionalInvestorsBuySell = kwargs.get("InstitutionalInvestorsBuySell", pd.DataFrame())
        # 外資持股
        self.Shareholding = kwargs.get("Shareholding", pd.DataFrame())
        # 此區塊請勿更動
        #-------------------------------------------------------------------
    
    def trade(self,date):
        ''' 
        此區塊，可進行資料處理、做技術指標，寫自己的策略，
        寫你自己的策略, 必須 return : 1 (買) or -1 (賣) or 0 (不操作)
        根據時間date，回傳當下要進行什麼操作 ( 買/賣/不操作 )
        '''
        # example
        from random import randint
        
        x = randint(1,10)
        x = x%3
        if x == 1:
            return 1
        elif x == 2:
            return -1
        elif x == 0:
            return 0
#------------------------------------------------------------------------------
            
def test():
    
    self = BackTest.BackTest(2316,user_funds = 5e5,year = 1)
    self.init_strategy(strategy = demo)
    self.selenium_everyday()
    self.cum_profit_plot()
    self.calculate_mean_profit_max_loss()

    print('mean profit {}'.format( self.mean_profit) )
    print('max loss {}'.format( self.max_loss) )
    print('now_profit {}'.format( self.now_profit) )

    print('mean profit per {}%'.format( self.mean_profit_per) )
    print('max loss per {}%'.format( self.max_loss_per) )
    print('now_profit per {}%'.format( self.now_profit_per) )
    