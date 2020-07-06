from .package_util.crawlIndex import CrawlIndex
from .package_util.crawlPlates import CrawlPlates
from .package_util.loadSymbol import loadSymbol
from .module.plate import Plate
import os
from pathlib import Path
import pandas as pd

class PlatesTool(Plate):
    def __init__(self):
        Plate.__init__(self)
        self.__symbols, self.__names = loadSymbol()
        self.__plateCrawl = CrawlPlates(self.__symbols, self.__names)
        self.__crawlIndex = CrawlIndex()

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

    def getOnePlateData(self, code):
        code = str(code)
        p = self.getFileBasePath() + '/plateData/'
        fileName = str(code) + ".csv"
        filePath = Path(p + fileName)
        print(filePath)

        if filePath.is_file():
            df = pd.read_csv(filePath)
            return df
        else:
            return None
