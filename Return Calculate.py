from pathlib import Path

import pandas

# Specify the folder path
folder_path = Path('History')

returnDict = {}

for f in folder_path.iterdir():
    child_path = Path(f)
    stockName = child_path.name.replace(".csv","")
    priceList = []
    print(f"Processing for {stockName}...")

    for c in child_path.iterdir():
        csvFile = pandas.read_csv(c)
        data = csvFile.shape[0]
        if data>0:
            pastPrice = csvFile.iloc[-1]['ltp ']
            newPrice = csvFile.iloc[0]['ltp ']
            newPrice = float(str(newPrice).replace(",",""))
            pastPrice = float(str(pastPrice).replace(",",""))
            timeRange = c.name.replace(stockName,"").replace(".csv","")

            priceList.append({timeRange:{'new':newPrice,'past':pastPrice}})

    returnDict[stockName] = priceList

for i in returnDict.keys():


    if len(returnDict[i])>1:
        firstData = (returnDict[i][0])
        lastData = (returnDict[i][-1])
        k1 = list(firstData.keys())[0]
        k2 = list(lastData.keys())[0]

        firstData = firstData[k1]['past']
        lastData = lastData[k2]['new']
        estimateReturn = round(((lastData/firstData)-1)*100,3)
        print(i)
        print(f"{k1} to {k2}")
        print("Return =",estimateReturn,"%")
        print("=" * 30)
