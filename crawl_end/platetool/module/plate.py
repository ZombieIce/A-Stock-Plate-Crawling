import os
import json
import requests
from pathlib import Path
import pandas as pd
from .formatUtil import formatTopStocks
from .crawler import Crawler

class Plate(Crawler):
    def __init__(self):
        super().__init__()
        self.__fileBasePath = str(os.path.abspath('.')) + '/Data'
        self.__baseURL = "https://pchq.kaipanla.com/w1/api/index.php"

    def __getPlateFileData(self, fileName):
        filePath = self.__fileBasePath + "/plateMap/" + fileName
        if os.path.exists(filePath):
            with open(filePath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        else:
            print(filePath + " does not exist!")
            return None
    
    def getAllStockPlateMapping(self):
        return self.__getPlateFileData("STOCKS_TO_PLATES.json")

    def getAllNormalPlates(self):
        return self.__getPlateFileData("NORMAL_TO_STOCKS.json")
    
    def getAllCarePlates(self):
        return self.__getPlateFileData("CARES_TO_STOCKS.json")

    def findOnePlateInfo(self, code):
        code = str(code)
        ctsMapInfo = self.getAllCarePlates()
        ntsMapInfo = self.getAllNormalPlates()
        if code in ctsMapInfo.keys():
            name = ctsMapInfo[code]["name"]
            stocks = ctsMapInfo[code]["stocks"]
            return {"code": code, "name": name, "stocks": stocks}
        elif code in ntsMapInfo.keys():
            name = ntsMapInfo[code]["name"]
            stocks = ntsMapInfo[code]["stocks"]
            return {"code": code, "name": name, "stocks": stocks}
        else:
            return None
        
    def getOnePlateData(self, code, lagDays=0):
        code = str(code)
        p = self.__fileBasePath + '/plateData/'
        fileName = str(code) + ".csv"
        filePath = Path(p + fileName)
        
        new_df = self.crawlOnePlate(code)
        old_df = None

        if filePath.is_file():
            old_df = pd.read_csv(filePath)
            new_df = pd.concat([old_df, new_df])

        lagMinutes = 241 * int(lagDays)
        if lagMinutes:
            return new_df[-lagMinutes:].to_json(orient='table')

        else:
            return new_df.to_json(orient='table')
