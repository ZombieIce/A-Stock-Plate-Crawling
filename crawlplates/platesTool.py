from .package_util.crawlIndex import CrawlIndex
from .package_util.crawlPlates import CrawlPlates
from .package_util.formatUtil import loadSymbol
import os
from pathlib import Path
import pandas as pd

class PlatesTool():
    def __init__(self):
        self.__symbols, self.__names = loadSymbol()
        self.__plateCrawl = CrawlPlates(self.__symbols, self.__names)
        self.__crawlIndex = CrawlIndex()
        self.__fileBasePath = str(os.path.abspath('.')) + '/Data'

    def setFileBasePath(self, p):
        if os.path.isdir(p):
            self.__fileBasePath = p
            self.__plateCrawl.setBasePath(p)
            self.__crawlIndex.setBasePath(p)
        else:
            raise Exception(p + " is not a direction")

    def __getFileBasePath(self):
        return self.__fileBasePath

    def updateData(self):
        p = self.__getFileBasePath()
        if not Path(p).is_dir():
            os.mkdir(p)
        print("Crawl Stocks Plates Map Info")
        self.__plateCrawl.crawlStockPlateData()
        print("\nCrawl All Plates Index Data")
        self.__crawlIndex.crawlAllPlatesData()
        