## PLATEHUNTER
 This package offers a class named **PlateHunter** which can get A Share Market plate data. (Need to modify end-server's IP address)
 1. **getOnePlateData**: return price volume data by the given plate code and lag days
   ```python
   ph.getOnePlateData(plate_code, lag_days)
   ```
 2. **getOnePlateInfo**: return plate name and stocks by the given plate code
   ```python
   ph.getOnePlateInfo(plate_code)
   ```
 3. **getTopConceptPlates**: return top 20 concept plates at the current time
   ```python
   ph.getTopConceptPlates()
   ```
 4. **getTopStocksInOnePlate**: return top 20 stocks in the given plates
   ```python
   ph.getTopStocksInOnePlate(plate_code)
   ```
 5. **getAllCarePlates**: return all care plates in the database
   ```python
   ph.getAllCarePlates()
   ```
 6. **getAllNormalPlates**: return all normal plates in the database
   ```python
   ph.getAllNormalPlates()
   ```
 7. **getAllStockPlateMap**: return all stock to their all normal plates and care plates
   ```python
   ph.getAllStockPlateMap()
   ```