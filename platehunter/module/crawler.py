import requests
import json
import pandas as pd
import datetime
from .formatUtil import formatTopStocks, topPlateFormat

class Crawler:
    def __init__(self):
        self.__baseURL = "https://pchq.kaipanla.com/w1/api/index.php"

    def getTopStocksInOnePlate(self, code):
        parameters = {"c": "PCArrangeData", "a": "GetZSHQPlate", "PStockID": code, "PlateID": code, "SelType": "4,2,3,1,5",
                    "UserID": 862892, "LType": 6, "Token": "8050e575cf13c8c5a108fbfa4e616d32", 
                    "LOrder": 1, "LIndex": 0, "Lst": 20}
        try:
            with requests.post(self.__baseURL, parameters, stream=True) as req:
                data = req.json()["stocks"]['list']
                return formatTopStocks(data)
        except Exception:
            return None

    def getTopConceptPlates(self):
        date = str(datetime.date.today())
        parameters = {"c": "PCArrangeData", "a": "GetZSIndexPlate", "SelType": "2,3", "Date": date,
                      "PType": "2", "POrder": "1", "ZSType": "5", "rate": "1", "PIndex": 0, "Pst": 20,
                      "LType": 6, "LOrder": 1, "LIndex": 0, "Lst": 20, "PlateID": 885853, "UserID": 862892,
                      "Token": "8050e575cf13c8c5a108fbfa4e616d32"}
        req = requests.post(self.__baseURL, data=parameters).json()['plates']['list']
        return topPlateFormat(req)