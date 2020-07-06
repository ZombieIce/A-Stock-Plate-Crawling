from ..module.stock import Stock
import json
import requests
import datetime
import sys
import os
from pathlib import Path
from ..package_util.formatUtil import stocksToJson, platesToJson
from requests.packages.urllib3.exceptions import InsecureRequestWarning

class CrawlPlates:
    def __init__(self, stockSymbols, stockNames):
        self.__stockSymbols = stockSymbols
        self.__stockNames = stockNames
        self.baseURL = "https://pchq.kaipanla.com/w1/api/index.php"
        self.__basePath = str(os.path.abspath('.')) + '/Data'
        self.__failedStocks = {}

    def setBasePath(self, p):
        self.__basePath = p
    
    def __parameterSettings(self, stockSymbol):
        parameters = {"c": "PCArrangeData", "a": "GetHQPlate", "StockID": stockSymbol, "SelType": "1,2,3,8,9",
                    "UserID": 862892, "Token": "8050e575cf13c8c5a108fbfa4e616d32", "Time":"09:30"}
        return parameters

    def __crawlOneStockData(self, stockSymbol, stockName):
        date = ''.join(str(datetime.date.today()).split('-'))
        para = self.__parameterSettings(stockSymbol)
        para['Day'] = date

        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        normalPlate = {"status": 200}
        carePlate = {"status": 200}

        try:
            with requests.post(self.baseURL, para, stream=True, verify=False) as req:
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
        except Exception as e:
            self.__failedStocks[stockSymbol] = stockName

        return normalPlate, carePlate

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
            st = Stock(self.__stockSymbols[i], self.__stockNames[i])
            np, cp = self.__crawlOneStockData(st.symbol, st.name)
            if np["status"] == 200:
                for k in np.keys():
                    if k != "status":
                        st.addStockPlate(k)
                        if k in NORMAL_TO_STOCKS:
                            NORMAL_TO_STOCKS[k].append(st.symbol)
                        else:
                            NORMAL_TO_STOCKS[k] = [np[k], st.symbol]

            if cp["status"] == 200:
                for k in cp.keys():
                    if k != "status":
                        st.addCarePlate(k)
                        if k in CARES_TO_STOCKS:
                            CARES_TO_STOCKS[k].append(st.symbol)
                        else:
                            CARES_TO_STOCKS[k] = [cp[k], st.symbol]
                        
            STOCKS_TO_PLATES[st.symbol] = st.formatPlateInfo()

            # progress visualization
            currProgress = round(i / (num-1) * 100, 1)
            print("\r", end="")
            print("Progress: {}%: ".format(currProgress), "▋" * (int(currProgress) // 2), end="")
            sys.stdout.flush()

        while self.__failedStocks != {}:
            currFailedStocks = self.__failedStocks
            self.__failedStocks = {}
            for (k, v) in currFailedStocks.items():
                st = Stock(k, v)
                np, cp = self.__crawlOneStockData(st.symbol, st.name)
                if np["status"] == 200:
                    for nk in np.keys():
                        if nk != "status":
                            st.addStockPlate(nk)
                            if nk in NORMAL_TO_STOCKS:
                                NORMAL_TO_STOCKS[nk].append(st.symbol)
                            else:
                                NORMAL_TO_STOCKS[nk] = [np[nk], st.symbol]

                if cp["status"] == 200:
                    for ck in cp.keys():
                        if ck != "status":
                            st.addCarePlate(ck)
                            if ck in CARES_TO_STOCKS:
                                CARES_TO_STOCKS[ck].append(st.symbol)
                            else:
                                CARES_TO_STOCKS[ck] = [cp[ck], st.symbol]
                            
                STOCKS_TO_PLATES[st.symbol] = st.formatPlateInfo()                



        cts = json.dumps(platesToJson(CARES_TO_STOCKS), indent=4)
        nts = json.dumps(platesToJson(NORMAL_TO_STOCKS), indent=4)
        stp = json.dumps(stocksToJson(STOCKS_TO_PLATES), indent=4)

        map_path = self.__basePath + '/plateMap/'
        if not Path(map_path).is_dir():
            os.mkdir(map_path)

        with open(map_path + 'CARES_TO_STOCKS.json', 'w', encoding="utf-8") as json_file:
            json_file.write(cts)

        with open(map_path + 'NORMAL_TO_STOCKS.json', 'w', encoding="utf-8") as json_file:
            json_file.write(nts)

        with open(map_path + 'STOCKS_TO_PLATES.json', 'w', encoding="utf-8") as json_file:
            json_file.write(stp)