import datetime
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

import pandas as pd
import requests


def fetch_stock(symbol):
    main_folder = Path(f"History/{symbol}")
    main_folder.mkdir(parents=True, exist_ok=True)
    base = Path("History")

    today_date = date.today()
    year_back_date = today_date - datetime.timedelta(days=365)

    session = requests.Session()
    headers = {
        "authority": "https://www.nseindia.com",
        "accept": "*/*",
        "accept-encoding": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "dnt": "1",
        "priority": "u=1, i",
        "referer": f"https://www.nseindia.com/get-quotes/equity?symbol={symbol}",
        "sec-ch-ua":'"Not)A;Brand";v = "8", "Chromium";v = "138", "Google Chrome";v = "138"',
        "sec-ch-ua-mobile":'?0',
        "sec-ch-ua-platform":"Windows",
        "sec-fetch-dest":"empty",
        "sec-fetch-mode":"cors",
        "sec-fetch-site":"same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    session.headers.update(headers)

    while True:
        cookies = session.get(headers['referer']).cookies  # Initialize cookies

        from_date = year_back_date.strftime('%d-%m-%Y')

        to_date = today_date.strftime('%d-%m-%Y')
        url = (f"https://www.nseindia.com/api/historical/cm/equity?symbol={symbol}"
            f"&series=[%22EQ%22]&from={from_date}&to={to_date}&csv=true")


        response = session.get(url,cookies=cookies)
        if response.status_code == 200 and len(response.content) > 2000:
            filename = main_folder / f"{symbol}_{year_back_date.year}_to_{today_date.year}.csv"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"✅ Saved: {filename}")

            # Move the window back by 1 year
            today_date = year_back_date
            year_back_date = today_date - datetime.timedelta(days=365)
        else:

            older_name = main_folder.stem
            (base / older_name).rename(base / f"{older_name}_completed")
            break


data = pd.read_csv("EQUITY_L.csv")['SYMBOL'].dropna().tolist()

try:
    completed = [i.stem.replace("_completed","") for i in Path("History").iterdir()
                 if 'completed' in i.stem]
    remaining = list(set(data) - set(completed))
    print(f"{len(completed)} stocks are already done. Remaining is {len(remaining)} stocks.")

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(fetch_stock, remaining)
except Exception as e:
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(fetch_stock, data)
