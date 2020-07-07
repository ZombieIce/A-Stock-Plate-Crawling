import pandas as pd
import tushare as ts

def loadSymbol():
    pro = ts.pro_api('eb952991aadb05a9d423224946dc09fc19c6ab4f1c673d72431e1fa1')
    data = pro.query('stock_basic', exchange='', list_status='L', fields='symbol,name')

    symbols = data['symbol'].to_list()
    names = data['name'].to_list()
        
    return symbols, names
