import json
import requests
url = "https://pchq.kaipanla.com/w1/api/index.php"
paras = {
    "c": "PCArrangeData",
    "a": "GetZSIndexPlate",
    "SelType": "2,3",
    "Date": "2020-07-06",
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

req = requests.post(url, data=paras).json()
print(req['plates']['list'])