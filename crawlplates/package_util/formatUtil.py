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

def topPlateFormat(data:list):
    topData = {"codes": [], "names": [], "increase": [],
                "rateOfIncrease": [], "mainNet": [],
                "mainBuy": [], "mainSell": [],
                "totalCirculationValue": []}
    for d in data:
        topData["codes"].append(d[0])
        topData["names"].append(d[1])
        topData["increase"].append(d[3])
        topData["rateOfIncrease"].append(d[4])
        topData["mainNet"].append(d[6])
        topData["mainBuy"].append(d[7])
        topData["mainSell"].append(d[8])
        topData["totalCirculationValue"].append(d[10])
    df = pd.DataFrame(topData)
    
    return df

def formatTopStocks(top):
    top_data = {"code": [], "name": [], "increase": [], "price": [],
                "totalCirculationValue": [], "volume": [], "mainNet": [],
                "mainBuy": [], "mainSell": [], "concept": []}
    for t in top:
        top_data['code'].append(t[0])
        top_data['name'].append(t[1])
        top_data['increase'].append(t[3])
        top_data['price'].append(t[2])
        top_data['totalCirculationValue'].append(t[7])
        top_data['volume'].append(t[4])
        top_data['mainNet'].append(t[10])
        top_data['mainBuy'].append(t[8])
        top_data['mainSell'].append(t[9])
        top_data['concept'].append(t[12])

    df = pd.DataFrame(top_data)
    return df