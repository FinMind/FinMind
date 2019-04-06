

TABLE = 'TaiwanStockInfo'

import pandas as pd
import os, sys
# __file__ = '/home/sam/project/github/package/FinMind/FinMind/Data/TaiwanStockInfo.py'
import platform
if 'Windows' in platform.platform():
    PATH = "\\".join( os.path.abspath(__file__).split('\\')[:-1])
else:
    PATH = "/".join( os.path.abspath(__file__).split('/')[:-1])
sys.path.append(PATH)
from BasedClass import query

class ClassTaiwanStockInfo:
    def __init__(self):
        pass

    def load_all(self,status = 'package'):
        colname = query( 'SHOW COLUMNS FROM {}'.format( TABLE ) )
        colname = [ c[0] for c in colname if c[0] not in  ['id','url'] ]     
        
        sql = 'select `{}` from {}'.format( '`,`'.join( colname ) ,TABLE)
        tem = query(sql)
        data = pd.DataFrame( list(tem) )
        data.columns = colname
        if status == 'package':
            sql = 'SHOW TABLES '
            #tem = query(sql,TABLE.replace('Info','Price'))
            tem = query(sql,'TaiwanStockPrice')
            stock_id = [ te[0].replace('_TW','') for te in tem ]
            bo = [ True if x in stock_id else False for x in data['stock_id'] ]
            data = data[bo]
            data.index = range(len(data))
        
        return data

def TaiwanStockInfo(select = [],date = '',status = 'package'):
    
    self = ClassTaiwanStockInfo()  
    data = self.load_all(status)
    #data = data[ data['status'] == 1 ]
    #del data['status']
    del data['crawler_date']
        
    return data


