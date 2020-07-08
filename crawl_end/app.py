from flask import Flask, request, jsonify
from platetool import PlatesTool

app = Flask(__name__)
pt = PlatesTool()

@app.route('/plateAPI', methods = ['POST'])
def plateAPI():
    if request.method == 'POST':
        listName = request.form['listName']
        code = request.form['code']
        lagDay = request.form['lagDay']
        if code:
            if lagDay:
                return pt.getOnePlateData(code, lagDay)
            else:
                return pt.findOnePlateInfo(code)
        else:
            listName = request.form['listName']
            if listName == 'cp':
                return pt.getAllCarePlates()
            if listName == 'np':
                return pt.getAllNormalPlates()
            if listName == 'stp':
                return pt.getAllStockPlateMapping()
        # return {'code': code, 'listName': listName, 'topStock': topStock, 'lagDay': lagDay}


if __name__ == "__main__":
    app.run()