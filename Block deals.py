import requests

def market_block_deals():

    session = requests.Session()
    headers = {
        "authority": "https://www.nseindia.com",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9,hi;q=0.8,bn;q=0.7",
        "dnt": "1",
        "priority": "u=0, i",
        "referer": "https://www.nseindia.com/market-data/stocks-traded",
        "sec-ch-ua":'"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        "sec-ch-ua-mobile":'?0',
        "sec-ch-ua-platform":"Windows",
        "sec-fetch-dest":"document",
        "sec-fetch-mode":"navigate",

        "sec-fetch-site":"same-origin",
       "sec-fetch-user":"?1",
        "upgrade-insecure-requests":"1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    session.headers.update(headers)
    cookies = session.get(headers['referer']).cookies  # Initialize cookies

    url = "https://www.nseindia.com/api/snapshot-capital-market-largedeal?objName=BLOCK_DEALS_DATA&fileName=BLOCK&csv=true"

    try:
        response = session.get(url,cookies=cookies)
        if response.status_code == 200:
            with open("file_block.csv", 'wb') as f:
                f.write(response.content)
                print("file saved...")
        else:
            print(response.status_code)
    except Exception as e:
        print(f"❌ Error fetching for market deals : {e}")


