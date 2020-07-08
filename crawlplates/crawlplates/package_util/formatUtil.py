import tushare as ts
import pandas as pd
import datetime
import time
import sys

# load stock symbol from tushare
def loadSymbol():
    pro = ts.pro_api('eb952991aadb05a9d423224946dc09fc19c6ab4f1c673d72431e1fa1')
    data = pro.query('stock_basic', exchange='', list_status='L', fields='symbol,name')
    symbols = data['symbol'].to_list()
    names = data['name'].to_list()
    return symbols, names

# execute for loop visualization
def visualTool(i, num):
    currProgress = round(i / (num-1) * 100, 1)
    print("\r", end="")
    print("Progress: {}%: ".format(currProgress), "▋" * (int(currProgress) // 2), end="")
    sys.stdout.flush()

# format plate basic information
def platesToJson(pts:dict):
    res = {}
    for (k, v) in pts.items():
        singleInfo = {"name": v[0], "stocks": v[1:]}
        res[k] = singleInfo
    return res

# format stock to plates mapping
def stocksToJson(stp:dict):
    res = {}
    for (k, v) in stp.items():
        singleInfo = {"name": v['name'], "normal_plates": v['stockPlate'], "care_plates": v['carePlate']}
        res[k] = singleInfo
    return res  

# format single plate price volume information
def plateData(data:list):
    date_time = []
    price = []
    volume = []
    date = "".join(str(datetime.datetime.now().date()).split("-"))
    for d in data:
        t = datetime.datetime.strptime(date + ''.join(d[0].split(':')), "%Y%m%d%H%M")
        date_time.append(t)
        price.append(d[1])
        volume.append(d[3])
    data = {"time": date_time, "price": price, "volume": volume}
    df = pd.DataFrame(data)
    return df