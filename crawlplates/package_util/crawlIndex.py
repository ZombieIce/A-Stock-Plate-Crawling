import json
import requests
import datetime
import sys
import os
from pathlib import Path
from .formatUtil import plateData, visualTool
import pandas as pd

class CrawlIndex:
    def __init__(self):
        self.__baseURL = "https://pchq.kaipanla.com/w1/api/index.php"
        self.__basePath = str(os.path.abspath('.')) + '/Data'
        self.__failedIndex = []

    def setBasePath(self, p):
        self.__basePath = p
    
    def __getPlateCode(self, isCare:bool):
        if isCare:
            fileName = '/plateMap/CARES_TO_STOCKS.json'
        else:
            fileName = '/plateMap/NORMAL_TO_STOCKS.json'
        filePath = self.__basePath + fileName
        if os.path.exists(filePath):
            with open(filePath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        else:
            print(filePath + " does not exist!")
            return None

    def __plateCodeList(self):
        carePlates = self.__getPlateCode(True)
        normalPlates = self.__getPlateCode(False)
        return list(carePlates.keys()) + list(normalPlates.keys())

    def __toFile(self, code, new_df):
        fileName = str(code) + ".csv"
        filePath = Path(self.__basePath + "/plateData/" + fileName)
        if filePath.is_file():
            new_df.to_csv(filePath, mode='a', index=None, header=False)
        else:
            new_df.to_csv(filePath, index=None)

    def __crawlOnePlate(self, code):
        parameters = {"c": "PCArrangeData", "a": "GetZSHQPlate", "StockID": code, "PStockID": code, "SelType": "4,1,5",
                    "UserID": 862892, "Token": "8050e575cf13c8c5a108fbfa4e616d32"}
        try:
            with requests.post(self.__baseURL, parameters, stream=True) as req:
                data = req.json()['trend']['trend']
                new_df = plateData(data)
        except Exception:
            self.__failedIndex.append(code)
            new_df = pd.DataFrame()
        return new_df

    def crawlAllPlatesData(self):
        plateList = self.__plateCodeList()
        dirPath = self.__basePath + "/plateData"
        if not Path(dirPath).is_dir():
            os.mkdir(self.__basePath + "/plateData")
        num = len(plateList)

        for i in range(num):
            curr_df = self.__crawlOnePlate(plateList[i])
            if curr_df.empty:
                continue
            self.__toFile(plateList[i], curr_df)
            visualTool(i, num)

        while len(self.__failedIndex) != 0:
            currFailedIndex = self.__failedIndex
            self.__failedIndex = []

            for c in currFailedIndex:
                curr_df = self.__crawlOnePlate(c)
                self.__toFile(c, curr_df)