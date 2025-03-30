import datetime
import time
from pathlib import Path
import requests
from concurrent.futures import ThreadPoolExecutor

def fetch_and_save_data(company_file, headers, nse_url):
    try:
        today = datetime.date.today()
        folder_name = Path(f'History/{company_file.stem}')

        if not folder_name.exists():
            folder_name.mkdir(parents=True)

        session = requests.Session()
        session.get(nse_url, headers=headers)  # Initialize session to get cookies
        cookies = session.cookies.get_dict()

        for _ in range(10):
            year1BACK = today - datetime.timedelta(days=365)
            criteria_url = (f"https://www.nseindia.com/api/historical/cm/equity?"
                            f"symbol={company_file.stem}&series=[%22EQ%22]&"
                            f"from={year1BACK.strftime('%d-%m-%Y')}&to={today.strftime('%d-%m-%Y')}&csv=true")

            response = session.get(criteria_url, headers=headers, cookies=cookies)

            if response.status_code == 200:
                file_path = folder_name / f"{company_file.stem} {year1BACK.strftime('%Y')}-{today.strftime('%Y')}.csv"
                with file_path.open("wb") as file:
                    file.write(response.content)
                print(f"File saved successfully: {file_path}")
                print("=" * 40)
                today -= datetime.timedelta(days=365)
            else:
                print(f"Failed to fetch data for {company_file.stem}. Status Code:", response.status_code)
                break

    except Exception as e:
        print(f"Error fetching data for {company_file.stem}: {e}")

def main():
    start = time.time()

    folder_path = Path('Companies')
    files = [f for f in folder_path.iterdir() if f.is_file()]

    nse_url = "https://www.nseindia.com"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.nseindia.com"
    }

    # Use ThreadPoolExecutor to fetch data in parallel
    with ThreadPoolExecutor() as executor:
        executor.map(lambda f: fetch_and_save_data(f, headers, nse_url), files)

    end = time.time()
    print(f"\nTime taken = {end - start} seconds")

if __name__ == "__main__":
    main()
