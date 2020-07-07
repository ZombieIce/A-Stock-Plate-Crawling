import json
import requests
import datetime
import sys
import os
from pathlib import Path
from .formatUtil import plateData
from ..module.plate import Plate
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import pandas as pd

class CrawlIndex:
    def __init__(self):
        self.__plate = Plate()
        self.__baseURL = "https://pchq.kaipanla.com/w1/api/index.php"
        self.__basePath = str(os.path.abspath('.')) + '/Data'
        self.__failedIndex = []

    def setBasePath(self, p):
        self.__basePath = p
        self.__plate.setFileBasePath(p)
    
    def __plateCodeList(self):
        carePlates = self.__plate.getAllCarePlate()
        normalPlates = self.__plate.getAllNormalPlate()
        return list(carePlates.keys()) + list(normalPlates.keys())

    def getTopStocksInOnePlate(self, code):
        parameters = {"c": "PCArrangeData", "a": "GetZSHQPlate", "PStockID": code, "PlateID": code, "SelType": "4,2,3,1,5",
                    "UserID": 862892, "LType": 6, "Token": "8050e575cf13c8c5a108fbfa4e616d32", 
                    "LOrder": 1, "LIndex": 0, "Lst": 20}
        
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        try:
            with requests.post(self.__baseURL, parameters, stream=True, verify=False) as req:
                data = req.json()["stocks"]["list"]
                return data
        except Exception as e:
            return None

    def __toFile(self, code, new_df):
        fileName = str(code) + ".csv"
        filePath = Path(self.__basePath + "/plateData/" + fileName)
        if filePath.is_file():
            new_df.to_csv(filePath, mode='a', index=None, header=False)
        else:
            new_df.to_csv(filePath, index=None)

    def crawlOnePlate(self, code):
        parameters = {"c": "PCArrangeData", "a": "GetZSHQPlate", "StockID": code, "PStockID": code, "SelType": "4,1,5",
                    "UserID": 862892, "Token": "8050e575cf13c8c5a108fbfa4e616d32"}
        
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        try:
            with requests.post(self.__baseURL, parameters, stream=True, verify=False) as req:
                data = req.json()['trend']['trend']
                
                # fileName = str(code) + ".csv"
                # filePath = Path(self.__basePath + "/plateData/" + fileName)

                new_df = plateData(data)
                # if filePath.is_file():
                #     new_df.to_csv(filePath, mode='a', index=None, header=False)
                # else:
                #     new_df.to_csv(filePath, index=None)
                return new_df
                    
        except Exception as e:
            self.__failedIndex.append(code)
            return None

    def crawlAllPlatesData(self):
        plateList = self.__plateCodeList()
        os.mkdir(self.__basePath + "/plateData")
        num = len(plateList)

        for i in range(num):
            curr_df = self.crawlOnePlate(plateList[i])
            if not curr_df:
                continue
            self.__toFile(plateList[i], curr_df)
            currProgress = round(i / (num-1) * 100, 1)
            print("\r", end="")
            print("Progress: {}%: ".format(currProgress), "▋" * (int(currProgress) // 2), end="")
            sys.stdout.flush()

        while len(self.__failedIndex) != 0:
            currFailedIndex = self.__failedIndex
            self.__failedIndex = []

            for c in self.__failedIndex:
                curr_df = self.crawlOnePlate(c)
                self.__toFile(c, curr_df)