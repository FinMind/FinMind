
TABLE = 'GoldPrice'

import os, sys
import pandas as pd
import platform
if 'Windows' in platform.platform():
    PATH = "\\".join( os.path.abspath(__file__).split('\\')[:-1])
else:
    PATH = "/".join( os.path.abspath(__file__).split('/')[:-1])
sys.path.append(PATH)
from BasedClass import execute_sql2

class ClassGoldPrice:

    def load(self,date):  
        colname = execute_sql2( 'SHOW COLUMNS FROM {}'.format( TABLE ) )
        colname = [ c[0] for c in colname if c[0] != 'id' ]                      
        
        sql = 'select `{}` from {}'.format( '`,`'.join( colname ) ,TABLE)
        
        if date != '':
            sql = "{} WHERE `date` >= '{}'".format(sql,date)
           
        data = execute_sql2( sql )
        data = pd.DataFrame(list(data))
        
        if len(data)>0:

            data.columns = colname
            data = data.sort_values('date')
                
            data.index = range(len(data))
            
        return data


def GoldPrice(select = [],date = ''):
    
    self = ClassGoldPrice()  
    data = self.load(date)
        
    return data


