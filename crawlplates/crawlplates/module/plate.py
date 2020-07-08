import time
from ..package_util.formatUtil import plateInfoFormat
import os
from pathlib import Path
import json
class Plate:
    def __init__(self):
        self.__fileBasePath = str(os.path.abspath('.')) + '/Data'
        
    def __getFileBasePath(self):
        return self.__fileBasePath
    
    def setFileBasePath(self, p):
        self.__fileBasePath = p

    def getAllCarePlate(self):
        fileName = '/plateMap/CARES_TO_STOCKS.json'
        filePath = self.__fileBasePath + fileName
        if os.path.exists(filePath):
            with open(filePath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        else:
            print(filePath + " does not exist!")
            return None

    def getAllNormalPlate(self):
        fileName = '/plateMap/NORMAL_TO_STOCKS.json'
        filePath = self.__fileBasePath + fileName
        if os.path.exists(filePath):
            with open(filePath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        else:
            print(filePath + " does not exist!")
            return None

    def findOnePlateInfo(self, code):
        code = str(code)
        ctsMapInfo = self.getAllCarePlate()
        ntsMapInfo = self.getAllNormalPlate()
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
