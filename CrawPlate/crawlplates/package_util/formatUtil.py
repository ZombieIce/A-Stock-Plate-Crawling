import pandas as pd
import datetime
import time

def platesToJson(pts:dict):
    res = {}
    for (k, v) in pts.items():
        singleInfo = {"name": v[0], "stocks": v[1:]}
        res[k] = singleInfo

    return res

def stocksToJson(stp:dict):
    res = {}
    for (k, v) in stp.items():
        singleInfo = {"name": v['name'], "normal_plates": v['stockPlate'], "care_plates": v['carePlate']}
        res[k] = singleInfo
    return res  

# return dict{code, name, stocks}
def plateInfoFormat(plateDBInfo:dict):
    return {"code":plateDBInfo["code"], "name":plateDBInfo["name"], "stocks":plateDBInfo["stocks"]}

def plateData(data:list):
    date_time = []
    price = []
    volume = []
    date = "".join(str(datetime.datetime.now().date()).split("-"))
    for d in data:
        date_time.append(date + ''.join(d[0].split(':')))
        price.append(d[1])
        volume.append(d[3])
    data = {"time": date_time, "price": price, "volume": volume}
    df = pd.DataFrame(data)
    return df
