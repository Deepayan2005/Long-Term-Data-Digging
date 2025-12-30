from concurrent.futures.thread import ThreadPoolExecutor

import requests
from bs4 import BeautifulSoup
import pandas
from pathlib import Path

def get_year(data : str):
    return data.split(' ')[-1]

def get_fundamentals(sym):
    folder = Path("Fundamentals")

    # Fetch a webpage
    url = f"https://www.screener.in/company/{sym}/consolidated/"
    response = requests.get(url)
    # Parse the HTML
    soup = BeautifulSoup(response.text, "html.parser")

    name = soup.find('h1', class_='h2 shrink-text').text

    timeline=[]

    profit_loss = (soup.find("section",attrs={'id':"profit-loss"})
                   .find('div',class_="responsive-holder fill-card-width"))

    balance_sheet = (soup.find("section",attrs={'id':"balance-sheet"}))

    for i in (profit_loss.find("thead").find_all("th")):
        if i.text.strip() != '' and i.text.strip().lower() != 'ttm':
            timeline.append(get_year(i.text.strip()))

    data1 = [i.text for i in profit_loss.find('tr',class_="stripe").find_all('td')][1:len(timeline)+1]
    sales = [float(i.replace(",","").strip()) for i in data1]
    data2 = [i for i in profit_loss.find_all("tr")][-3]
    data3 = [i.text for i in data2.find_all('td')][1:len(timeline)+1]
    data4 =[i for i in profit_loss.find_all("tr")][-2]
    data4 =[i.text for i in data4.find_all('td')][1:len(timeline)+1]
    eps = []
    for i in data4:
        c = i.replace(",","").strip()
        if c!='':
            eps.append(float(c))
        else:eps.append(0)

    net_profit = []

    for i in data3:
        c = i.replace(",","").strip()
        if c!='':
            net_profit.append(float(c))
        else:net_profit.append(0)

    data_items = balance_sheet.find('tbody').find_all('tr')
    equity = []
    reserves = []
    debt = []

    rows = [equity, reserves, debt]

    for row_index, target_list in enumerate(rows):
        for td in data_items[row_index].find_all('td')[1:]:
            value = (td.get_text(strip=True).replace(",", ""))
            if value!='':
                target_list.append(float(value))
            else:
                target_list.append(0)


    ratio_DebtEquity = []


    for d, e, r in zip(debt, equity, reserves):
        if e>0 and r> 0:
            ratio_DebtEquity.append(round((d / (e + r)), 3))
        else:
            ratio_DebtEquity.append(0)

    roe_ratio=[]


    for n, e, r in zip(net_profit, equity, reserves):
        if (e > 0) and (r> 0):
            roe_ratio.append(round(n / (e + r), 2) )
        else: roe_ratio.append(0)

    table = {"year":timeline,'profit':net_profit[:len(timeline)],
             'sales':sales[:len(timeline)],'equity':equity[:len(timeline)],
             "reserves":reserves[:len(timeline)],"debt":debt[:len(timeline)],
             "DE-ratio":ratio_DebtEquity[:len(timeline)],"Eps":eps[:len(timeline)],
             "ROE":roe_ratio[:len(timeline)]}

    check_sizes = [len(table[i]) for i in table.keys()]

    if max(check_sizes)==min(check_sizes):
        dataFrame = pandas.DataFrame(table)
        dataFrame.to_csv(f"{folder.absolute()}/{sym}.csv",index=False)
        print(f"{sym} saved. ({name})")
    else:
        print(url)
        print(f"Unequal sizes in {sym}.")

data = pandas.read_csv("EQUITY_L.csv")['SYMBOL'].dropna().tolist()

Path("Fundamentals").mkdir(exist_ok=True)

completed = [i.stem for i in Path("Fundamentals").iterdir()]
remaining = list(set(data) - set(completed))
print(f"{len(completed)} stocks are already done | Remaining is {len(remaining)} stocks | {round(len(completed)/len(data),4)*100}% complete")

print(remaining)

with ThreadPoolExecutor(max_workers=20) as executor:

    executor.map(get_fundamentals, remaining)

