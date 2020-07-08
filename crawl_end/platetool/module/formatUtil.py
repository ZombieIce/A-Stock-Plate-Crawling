import pandas as pd
import datetime

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

def plateData(data:list):
    date_time = []
    price = []
    volume = []
    date = str(datetime.datetime.now().date())
    for d in data:
        date_time.append(date + ' ' + d[0])
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