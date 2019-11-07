

def trade(
        user_funds,
        user_stock,
        stock_price,
        volume,
        trade,
        tax,
        fee):
    '''
    example : 
        input : 
            user_funds = 200
            stock_price = 85.0
            stock_cost = stock_price
            tax = 0.005
            fee = 0.005
            volume = 2000
            trade = 1 #(1 is buy, -1 is sell)
            user_stock = stock('2317',1000,230, 310).__dict__ # 張數，成本, 現價
            
        output : 
            user_funds = user_funds - stock_price
            UnrealizedProfit = stock_price*(1-tax-fee) - stock_cost
            realizedProfit = 0
            everytime_profit = UnrealizedProfit + realizedProfit
            user_stock = 1
    '''
    if trade == 1:# buy
        '''
        1. 買股票，資金減少，股票增加
        2. 買新股票，成本等於，mean( 舊股票成本, 新股票成本 )
        3. 未實現損益 = 現價扣除手續費、稅金後，減掉成本
        '''
        # 資金減少
        user_funds = user_funds - user_stock['price']*volume
        # 買新股票，成本等於，mean( 舊股票成本, 新股票成本 )
        origin_cost = user_stock['volume']*user_stock['cost']
        new_cost = user_stock['price']*volume
        # 股票增加
        user_stock['volume'] += volume
        user_stock['cost'] =  (origin_cost + new_cost)/user_stock['volume']

    elif trade == -1:# sell
        '''
        賣股票，資金增加，股票減少
        賣股票，成本不需重算，
        賣股票，開始計算已實現損益
        已實現損益 : 現價扣除手續費、稅金後，減去成本
        '''
        # 資金增加,
        user_funds = user_funds + user_stock['price']*volume*(1-tax-fee)
        # 已實現損益 : 現價扣除手續費、稅金後，減去成本
        user_stock['realizedProfit'] += round(
            ( user_stock['price']*(1-tax-fee) - user_stock['cost'] )*volume,2 )
        # 股票減少
        user_stock['volume'] -= volume
            
    # 未實現獲利, 每次都要算
    user_stock['UnrealizedProfit'] = round(
        ( user_stock['price']*(1-tax-fee) - user_stock['cost'] )*user_stock['volume'],2 )
    
    # 每個時段的獲利，提供 user 隨時都想出場的報酬，
    user_stock['everytime_profit'] = \
        user_stock['UnrealizedProfit'] + user_stock['realizedProfit']
    
    return user_funds,user_stock
        
class stock:
    def __init__(self,stock_id,volume, cost, price):
        self.stock_id = stock_id
        self.volume = volume
        self.cost = cost
        self.price = price
        self.UnrealizedProfit = 0
        self.realizedProfit = 0
        self.everytime_profit = 0
        