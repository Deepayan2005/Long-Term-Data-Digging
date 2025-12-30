from pathlib import Path

import requests
from bs4 import BeautifulSoup


def get_year(data : str):
    return data.split(' ')[-1]

def get_fundamentals(sym):
    folder = Path("Fundamentals")

    # Fetch a webpage
    url = f"https://ticker.finology.in/company/{sym}?mode=C"
    print(url)
    response = requests.get(url)

    # Parse the HTML
    soup = BeautifulSoup(response.text, "html.parser")
    name = soup.find("span",attrs={'id':"mainContent_ltrlCompName"}).text
    print(name)
    timeline=[get_year(i.text) for i in soup.find('div',attrs={"id":"profit"}).find('table')
                            .find('thead').find_all('th')[1:]]
    rows1 = [i for i in soup.find('div',attrs={"id":"profit"}).find('table')
                            .find('tbody').find_all('tr')]
    rows2 = [i for i in soup.find('div', attrs={"id": "balance"}).find('table')
                            .find('tbody').find_all('tr')]
    sales = [float(i.text.replace("\r","").replace("\n","").replace(" ",""))
             for i in rows1[0].find_all("td")]
    net_profit=[float(i.text.replace("\r","").replace("\n","").replace(" ",""))
             for i in rows1[-2].find_all("td")]
    eps = [float(i.text.replace("\r","").replace("\n","").replace(" ",""))
             for i in rows1[-1].find_all("td")]
    equity = [float(i.text.replace("\r", "").replace("\n", "").replace(" ", ""))
           for i in rows2[1].find_all("td")]
    reserves = [float(i.text.replace("\r", "").replace("\n", "")
                      .replace(" ", ""))
              for i in rows2[2].find_all("td")]
    borrowings = [float(i.text.replace("\r", "").replace("\n", "")
                                .replace(" ", ""))
                          for i in rows2[4].find_all("td")]
    others_liabilities=[float(i.text.replace("\r", "").replace("\n", "")
                      .replace(" ", ""))
              for i in rows2[5].find_all("td")]

    debt = [(b+o) for b,o in zip(borrowings,others_liabilities)]

    print("Years =",timeline)
    print("Sales =",sales)
    print("Net Profit =",net_profit)
    print("EPS =",eps)
    print("Equity =",equity)
    print("Reserves =",reserves)
    print("Debt =",debt)
    print("Borrowings =",borrowings)
    print("Other Liabilities =",others_liabilities)





get_fundamentals("SBIN")