from crawlplates import PlatesTool
import tushare as ts
from datetime import datetime
import sys

if __name__ == "__main__":
    if ts.is_holiday(datetime.strftime(datetime.now(), '%Y-%m-%d')):
        sys.exit(0)
    pt = PlatesTool()
    pt.setFileBasePath("YOUR DATABASE DIRECTION")
    pt.updateData()
