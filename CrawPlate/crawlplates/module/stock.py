class Stock:
    def __init__(self, symbol, name):
        self.__name = name
        self.__symbol = symbol
        self.__stockPlate = []
        self.__carePlate = []

    @property
    def name(self):
        return self.__name

    @property
    def symbol(self):
        return self.__symbol

    @property
    def stockPlate(self):
        return self.stockPlate

    @property
    def carePlate(self):
        return self.__carePlate

    def addCarePlate(self, cp):
        if cp in self.__carePlate:
            print("Already exist!")
        else:
            self.__carePlate.append(cp)

    def addStockPlate(self, sp):
        if sp in self.__stockPlate:
            print("Already exist!")
        else:
            self.__stockPlate.append(sp)
            # print("Success")
    
    def formatPlateInfo(self):
        # print(self.__carePlate)
        return {"name": self.__name, "carePlate":self.__carePlate, "stockPlate": self.__stockPlate}