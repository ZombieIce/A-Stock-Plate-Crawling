from .package_util.crawlIndex import CrawlIndex
from .package_util.crawlPlates import CrawlPlates
from .package_util.loadSymbol import loadSymbol
from .package_util.crawlConcept import CrawlConcept
from .module.plate import Plate
from .package_util.formatUtil import plateData, formatTopStocks
import os
from pathlib import Path
import pandas as pd

class PlatesTool(Plate):
    def __init__(self):
        Plate.__init__(self)
        self.__symbols, self.__names = loadSymbol()
        self.__plateCrawl = CrawlPlates(self.__symbols, self.__names)
        self.__crawlIndex = CrawlIndex()
        self.__crawlConcept = CrawlConcept()

    def setFileBasePath(self, p):
        if os.path.isdir(p):
            super().setFileBasePath(p)
            self.__plateCrawl.setBasePath(p)
            self.__crawlIndex.setBasePath(p)
        else:
            raise Exception(p + " is not a direction")

    def updateData(self):
        p = self.getFileBasePath()
        if not Path(p).is_dir():
            os.mkdir(p)
        print("Crawl Stocks Plates Map Info\n")
        self.__plateCrawl.crawlStockPlateData()
        print("\nCrawl All Plates Index Data\n")
        self.__crawlIndex.crawlAllPlatesData()
        print()

    def getOnePlateData(self, code, lagDays=0):
        code = str(code)
        p = self._Plate__getFileBasePath() + '/plateData/'
        fileName = str(code) + ".csv"
        filePath = Path(p + fileName)
        
        new_df = self.__crawlIndex.crawlOnePlate(code)
        old_df = None

        if filePath.is_file():
            old_df = pd.read_csv(filePath)

        new_df = pd.concat([new_df, old_df])

        lagMinutes = 241 * lagDays
        if lagMinutes:
            return new_df[:lagMinutes]
        return new_df

    def getTopConceptPlates(self):
        return self.__crawlConcept.getTopConceptPlates()

    def getTopStocksInOnePlate(self, code):
        top =  self.__crawlIndex.getTopStocksInOnePlate(code)
        return formatTopStocks(top)
        