from module.crawler import Crawler
import requests
import pandas as pd

class PlateHunter(Crawler):
    def __init__(self):
        super().__init__()
        self.__remote = "http://127.0.0.1:5000/plateAPI"
        self.__form = {"code": "", "listName": "", "lagDay": ""}

    def __resetForm(self):
        self.__form = {"code": "", "listName": "", "lagDay": ""}

    def getOnePlateData(self, code, lagDay):
        self.__resetForm()
        self.__form["code"] = code
        self.__form["lagDay"] = lagDay
        req = requests.post(self.__remote, self.__form).json()['data']
        data = {'time':[], 'price':[], 'volume':[]}
        for d in req:
            data['time'].append(d['time'])
            data['price'].append(d['price'])
            data['volume'].append(d['volume'])
        df = pd.DataFrame(data)
        return df

    def getOnePlateInfo(self, code):
        self.__resetForm()
        self.__form["code"] = code
        req = requests.post(self.__remote, self.__form).json()
        return req

    def getAllCarePlates(self):
        self.__resetForm()
        self.__form["listName"] = "cp"
        req = requests.post(self.__remote, self.__form).json()
        return req

    def getAllNormalPlates(self):
        self.__resetForm()
        self.__form["listName"] = "np"
        req = requests.post(self.__remote, self.__form).json()
        return req

    def getAllStockPlateMap(self):
        self.__resetForm()
        self.__form["listName"] = "stp"
        req = requests.post(self.__remote, self.__form).json()
        return req

ph = PlateHunter()
print(ph.getTopConceptPlates())
print(ph.getTopStocksInOnePlate(885860))
print(ph.getOnePlateData(885795, 1))
print(ph.getOnePlateInfo(885860))
print(ph.getAllCarePlates())
print(ph.getAllNormalPlates())
print(ph.getAllStockPlateMap())
