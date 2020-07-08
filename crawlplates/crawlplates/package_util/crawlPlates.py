from ..module.stock import Stock
import json
import requests
import datetime
import sys
import os
from pathlib import Path
from ..package_util.formatUtil import stocksToJson, platesToJson, visualTool

class CrawlPlates:
    def __init__(self, stockSymbols, stockNames):
        self.__stockSymbols = stockSymbols
        self.__stockNames = stockNames
        self.__baseURL = "https://pchq.kaipanla.com/w1/api/index.php"
        self.__basePath = str(os.path.abspath('.')) + '/Data'
        self.__failedStocks = {}

    # custom storage direction
    def setBasePath(self, p):
        self.__basePath = p
    
    # crawl script baisc parameter
    def __parameterSettings(self, stockSymbol):
        parameters = {"c": "PCArrangeData", "a": "GetHQPlate", "StockID": stockSymbol, "SelType": "1,2,3,8,9",
                    "UserID": 862892, "Token": "8050e575cf13c8c5a108fbfa4e616d32", "Time":"09:30"}
        return parameters

    # crawl single stock to get normal plates and care plates
    def __crawlOneStockData(self, stockSymbol, stockName):
        date = ''.join(str(datetime.date.today()).split('-'))
        para = self.__parameterSettings(stockSymbol)
        para['Day'] = date

        normalPlate = {"status": 200}
        carePlate = {"status": 200}

        try:
            with requests.post(self.__baseURL, para, stream=True) as req:
                data = req.json()
                
                normalPlateData = data['stockplate']
                carePlateData = data['careplate']

                if normalPlateData == None:
                    normalPlate["status"] = 404
                else:
                    for sp in normalPlateData:
                        normalPlate[sp[-1]] = sp[0]

                if carePlateData == None:
                    carePlate["status"] = 404
                else:
                    for cp in carePlateData:
                        carePlate[cp[-1]] = cp[0]
        except Exception:
            self.__failedStocks[stockSymbol] = stockName

        return normalPlate, carePlate

    # divide data into three storage format
    def __classifyCrawlData(self, symbol, name, cts, nts, stp):
        st = Stock(symbol, name)
        np, cp = self.__crawlOneStockData(symbol, name)
        self.__classifyHelper(np, st, nts, False)
        self.__classifyHelper(cp, st, cts, True)
        stp[symbol] = st.formatPlateInfo()

    # single stock divide helper
    def __classifyHelper(self, plates:dict, st:Stock, ts:dict, isCare:bool):
        if plates['status'] == 200:
            for k in plates.keys():
                if k != 'status':
                    if isCare:
                        st.addCarePlate(k)
                    else:
                        st.addStockPlate(k)
                    if k in ts:
                        ts[k].append(st.symbol)
                    else:
                        ts[k] = [plates[k], st.symbol]

    # write crawling data into json file
    def __jsonToFile(self, path, fileName, file):
        with open(path + fileName, 'w', encoding="utf-8") as json_file:
            json_file.write(file)    

    # stock & plates code records
    # plates struct:
    #   key: code
    #   value: list[] [0] name [1:] stock code
    def crawlStockPlateData(self):
        # stocks in care plate -> dict: plateName: stocks.
        CARES_TO_STOCKS = {}
        # stocks in normal plate -> dict: plateName: stocks
        NORMAL_TO_STOCKS = {}
        # stock belongs to plates
        STOCKS_TO_PLATES = {}

        num = len(self.__stockSymbols)

        for i in range(num):
            self.__classifyCrawlData(self.__stockSymbols[i], self.__stockNames[i], CARES_TO_STOCKS, NORMAL_TO_STOCKS, STOCKS_TO_PLATES)
            visualTool(i, num)

        while self.__failedStocks != {}:
            currFailedStocks = self.__failedStocks
            self.__failedStocks = {}
            for (k, v) in currFailedStocks.items():
                self.__classifyCrawlData(k, v, CARES_TO_STOCKS, NORMAL_TO_STOCKS, STOCKS_TO_PLATES)              

        cts = json.dumps(platesToJson(CARES_TO_STOCKS), indent=4)
        nts = json.dumps(platesToJson(NORMAL_TO_STOCKS), indent=4)
        stp = json.dumps(stocksToJson(STOCKS_TO_PLATES), indent=4)

        map_path = self.__basePath + '/plateMap/'
        if not Path(map_path).is_dir():
            os.mkdir(map_path)

        self.__jsonToFile(map_path, 'CARES_TO_STOCKS.json', cts)
        self.__jsonToFile(map_path, 'NORMAL_TO_STOCKS.json', nts)
        self.__jsonToFile(map_path, 'STOCKS_TO_PLATES.json', stp)
