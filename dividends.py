from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pandas
import pandas as pd
import requests


def get_dividends(symbol):
    main_folder = Path("Dividends")
    main_folder.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    headers = {
        "authority": "https://www.nseindia.com",
        "accept": "*/*",
        "accept-encoding": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "dnt": "1",
        "priority": "u=1, i",
        "referer": f"https://www.nseindia.com/companies-listing/corporate-filings-actions?symbol={symbol}&tabIndex=equity",
        "sec-ch-ua": '"Not)A;Brand";v = "8", "Chromium";v = "138", "Google Chrome";v = "138"',
        "sec-ch-ua-mobile": '?0',
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    session.headers.update(headers) # Initialize cookies
    cookies = session.get(headers['referer']).cookies  # Initialize cookies

    url = ("https://www.nseindia.com/api/corporates-corporateActions?index=equities"+
           f"&symbol={symbol}&subject=Dividend&csv=true")

    response = session.get(url,cookies=cookies)
    if response.status_code == 200:
        with open(f"Dividends/{symbol}_dividend.csv", 'wb') as f:
            f.write(response.content)
            print(f"Dividend file for {symbol} saved.")
            check_file = Path("completed.csv")

            if not check_file.exists():
                dataset = {"Completed": [symbol]}
                temp_file = pandas.DataFrame(dataset)
                temp_file.to_csv(check_file, index=False)
            else:
                dataset = pandas.read_csv(check_file)
                if symbol not in dataset['Completed'].values:
                    dataset.loc[len(dataset)] = [symbol]
                dataset.to_csv(check_file, index=False)

    else:
        print(response.status_code)

data = pd.read_csv("EQUITY_L.csv")['SYMBOL'].dropna().tolist()

try:
    completed = pd.read_csv("completed.csv")['Completed'].dropna().tolist()
    remaining = list(set(data) - set(completed))
    print(f"{len(completed)} stocks are already done. Remaining is {len(remaining)} stocks.")

    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(get_dividends, remaining)
except Exception as e:
    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(get_dividends, data)