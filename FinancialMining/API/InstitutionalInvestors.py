
TABLE = 'InstitutionalInvestors'

import os, sys
import pandas as pd
PATH = "/".join( os.path.abspath(__file__).split('/')[:-2])
sys.path.append(PATH)
from API.BasedClass import execute_sql2

class ClassInstitutionalInvestors:

    def load(self,date):  
        colname = execute_sql2( 'SHOW COLUMNS FROM {}'.format( TABLE ) )
        colname = [ c[0] for c in colname if c[0] != 'id' ]                      
        
        sql = 'select `{}` from {}'.format( '`,`'.join( colname ) ,TABLE)
        
        if date != '':
            sql = "{} WHERE `date` > '{}'".format(sql,date)
           
        data = execute_sql2( sql )
        data = pd.DataFrame(list(data))
        
        if len(data)>0:

            data.columns = colname
            if 'stock_id' in data.columns:
                data = data.sort_values(['stock_id','date'])
            else:
                data = data.sort_values('date')
                
            data.index = range(len(data))
            
        return data


def InstitutionalInvestors(select = [],date = ''):
    
    self = ClassInstitutionalInvestors()  
    data = self.load(date)
        
    return data

