

import pandas as pd
import pymysql
HOST = '103.29.68.107'
USER = 'guest'
PASSWORD = '123'
DATABASE = 'FinancialData'

#---------------------------------------------------------
def execute_sql2(sql,database = DATABASE):
    
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
class Load:
    def __init__(self,table,select_variable):
        self.table = table
        self.select_variable = select_variable
    
    def get_data_list(self):
        sql = " SELECT DISTINCT `{}` FROM `{}`  ".format(self.select_variable,self.table)
        tem = execute_sql2( sql )
        data_list = [ te[0] for te in tem ]
        data_list.sort()
        return  data_list   
    
    def load(self,select = '',date = ''):
        
        colname = execute_sql2( 'SHOW COLUMNS FROM {}'.format( self.table ) )
        colname = [ c[0] for c in colname if c[0] not in  ['id','url','data_id','ISIN'] ]              
        
        sql = 'select `{}` from {}'.format( '`,`'.join( colname ) ,self.table)
        
        if select != '' or date != '':
            sql = "{} WHERE ".format(sql)

        bool_and = ''
        if select != '' and date != '':
            bool_and = 'AND'

        if select != '': 
            select = " `{}` = '{}' {}".format(self.select_variable,select,bool_and)
        if date != '': 
            date = " `date` >= '{}' ".format(date)
        
        sql = sql + select + date
           
        data = execute_sql2( sql )
        data = pd.DataFrame(list(data))
        if len(data)>0:
            
            data.columns = colname
            
            if self.select_variable in data.columns:
                data = data.sort_values([self.select_variable,'date'])
            else:
                data = data.sort_values('date')
                
            data.index = range(len(data))
            
        return data
    
    def load_multi(self,select_list = [],date = ''):
        
        data = pd.DataFrame()
        for select in select_list:
            data = data.append( self.load(select = select,date = date) )
        data.index = range(len(data))
        return data

