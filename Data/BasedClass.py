

import pandas as pd
import pymysql
import numpy as np
HOST = '103.29.68.107'
USER = 'guest'
PASSWORD = '123'
DATABASE = 'FinancialData'

#---------------------------------------------------------
def query(sql,database = DATABASE):
    
    conn = ( pymysql.connect(host = HOST,
                     port = 3306,
                     user = USER,
                     password = PASSWORD,
                     database = database, 
                     charset="utf8") )
                             
    cursor = conn.cursor()    

    try:   
        cursor.execute(sql)
        data = cursor.fetchall()
        conn.close()
        return data
    except:
        conn.close()
        return ''    
#---------------------------------------------------------
# based class 
# self = Load('TaiwanStockMarginPurchaseShortSale','stock_id')        
class Load:
    def __init__(self,table,select_variable):
        self.table = table
        self.select_variable = select_variable
    
    def get_data_list(self):
        sql = " SELECT DISTINCT `{}` FROM `{}`  ".format(self.select_variable,self.table)
        tem = query( sql )
        data_list = [ te[0] for te in tem ]
        data_list.sort()
        return  data_list   
    
    def load(self,select = '',date = ''):
        
        colname = query( 'SHOW COLUMNS FROM {}'.format( self.table ) )
        colname = [ c[0] for c in colname if c[0] not in  ['id','url','data_id','ISIN'] ]              
        
        sql = """ SELECT `{}` from `{}` 
                    WHERE `{}` = '{}'
                    AND `date` >= '{}'
                """.format( '`,`'.join( colname ) ,self.table,self.select_variable,select,date)

        data = query( sql )
        data = pd.DataFrame(list(data))
        if len(data)>0:
            
            data.columns = colname
            if self.select_variable in data.columns:
                data = data.sort_values([self.select_variable,'date'])
            else:
                data = data.sort_values('date')

        return data
    
    def load_multi(self,select_list = [],date = ''):
        
        data = pd.DataFrame()
        for select in select_list:
            data = data.append( self.load(select = select,date = date) )
        data.index = range(len(data))
        return data
    
    
    def transpose(self,data):
        date = list( np.unique(data['date']) )
        data1 = pd.DataFrame()
        select_var_list = list( np.unique(data[self.select_variable]) )
        
        for d in date:# d = date[0]
            #data1 = data[]
            for select_var in select_var_list:
                data2 = data.loc[(data['date']==d) & ( data[self.select_variable] == select_var ),
                                 ['type','value']]
                data2.index = data2['type']
                del data2['type']
                data2 = data2.T
                data2.index = range(len(data2))
                data2.columns = list(data2.columns)
                data2['stock_id'] = select_var
                data2['date'] = d
                data1 = data1.append(data2)    
                
        data1.index = range(len(data1))
        return data1
    

