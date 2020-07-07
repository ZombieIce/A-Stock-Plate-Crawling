import requests
import datetime
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import pandas as pd
from .formatUtil import topPlateFormat

class CrawlConcept:
    def __init__(self):
        self.__url = "https://pchq.kaipanla.com/w1/api/index.php"
        self.__basePath = str(os.path.abspath('.')) + '/Data'
        self.__curTopList = []

    def setBasePath(self, p):
        self.__basePath = p

    def __parameterSetting(self):
        date = str(datetime.date.today())
        parameters = {
            "c": "PCArrangeData",
            "a": "GetZSIndexPlate",
            "SelType": "2,3",
            "Date": date,
            "PType": "2",
            "POrder": "1",
            "ZSType": "5",
            "rate": "1",
            "PIndex": 0,
            "Pst": 20,
            "LType": 6,
            "LOrder": 1,
            "LIndex": 0,
            "Lst": 20,
            "PlateID": 885853,
            "UserID": 862892,
            "Token": "8050e575cf13c8c5a108fbfa4e616d32"
        }
        return parameters

    def getTopConceptPlates(self):
        para = self.__parameterSetting()
        req = requests.post(self.__url, data=para).json()['plates']['list']
        
        return topPlateFormat(req)
    