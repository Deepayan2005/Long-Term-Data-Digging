import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import reportmaker
import statistics
import math

def get_ROCE(profit, equity, debt):
    try:
        return (profit / (equity + debt)) * 100
    except ZeroDivisionError:
        return 0


def cagr(series, years):
    if len(series) < years + 1:
        return None

    start = series[-(years + 1)]
    end = series[-1]

    if start <= 0 or end <= 0:
        return None

    return (end / start) ** (1 / years) - 1


def generate_report_config(path: Path):
    try:

        df = pd.read_csv(path)
        if df.empty:
            return None

        name = path.stem

        df["profit_change%"] = (
            (df["profit"] - df["profit"].shift(1)) / df["profit"].shift(1).abs()
        ) * 100

        df["sales_change%"] = (
            (df["sales"] - df["sales"].shift(1)) / df["sales"].shift(1).abs()
        ) * 100

        df = df.fillna(0)

        base = Path(__file__).parent
        avg_file = base / "Averages" / f"{name}.csv"
        avg_df = pd.read_csv(avg_file).fillna(0)

        avg = avg_df["average"].tolist()
        profit = df["profit"].tolist()
        sales = df["sales"].tolist()
        sales_change = df["sales_change%"].tolist()
        eps = df["Eps"].tolist()
        de_ratio = df["DE-ratio"].tolist()
        roce=[get_ROCE(p, e, d) for p, e, d in zip(df["profit"], df["equity"], df["debt"])]

        config = {
            "name": name,
            "avg_years": avg_df["year"].tolist(),
            "avg": avg,
            "parameter_year": df["year"].tolist(),
            "profit": profit,
            "profit_change": df["profit_change%"].tolist(),
            "sales": sales,
            "sales_change": sales_change,
            "eps": eps,
            "de_ratio": de_ratio,
            "roce": roce
        }



        if (len(avg) >= 10 and avg[-1]>3*avg[-5]):

            print(f"{name} is suitable for investing.")
            return config
        else:
            print(f"{name} does not pass the criteria !")
            return None

    except Exception as e:
        print(f"[DATA ERROR] {path.name}: {e}")
        return None

def make_report(details: dict):

    drm = reportmaker.DataReportMaker(details["name"], details, Path(__file__).parent/'Reports')
    drm.put_graph_image(
        f"Average Stock Price({details["name"]})","Year", "AVG Price",
        "avg_years", "avg","line", (10, 10))

    drm.put_graph_image(
        f"Debt-Equity (DE) Ratio ({details["name"]})","Year", "DE ratio",
        "parameter_year", "de_ratio","bar", (150, 10),colors=True)

    drm.put_graph_image(
        f"Profit Per Year (Crore) ({details["name"]})","Year", "Profit",
        "parameter_year", "profit","bar", (10, 110), colors=True
    )

    drm.put_graph_image(
        f"Profit Change % ({details["name"]})","Year", "Profit Change %",
        "parameter_year", "profit_change","bar", (150, 110), colors=True
    )

    drm.put_graph_image(
        f"Sales (Crore) ({details["name"]})","Year", "Sales",
        "parameter_year", "sales","bar", (10, 10), colors=True
    )

    drm.put_graph_image(
        f"Sales Change % ({details["name"]})","Year", "Sales Change %",
        "parameter_year", "sales_change","bar", (150, 10), colors=True
    )

    drm.put_graph_image(
        f"Earning Per Share ({details["name"]})","Year", "EPS",
        "parameter_year", "eps","bar", (10, 110), colors=True
    )

    drm.put_graph_image(
        f"Return On Capital Employed % ({details["name"]})","Year", "ROCE%",
        "parameter_year", "roce","bar", (150, 110), colors=True
    )

    drm.save_file()


base = Path(__file__).parent
fundamentals = base / "Fundamentals"

folder_1 = {f'{i.stem}':i for i in fundamentals.iterdir()}
folder_2 = {f'{i.stem}':i for i in (base/"Averages").iterdir()}\

Path(base/'Reports').mkdir(exist_ok=True)

reports = [i.stem for i in (base/"Reports").iterdir()]


result = list(set(set(folder_1.keys()) & set(folder_2.keys()))-set(reports))

remaining_files = [folder_1[i] or folder_2[i] for i in result]

with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
    configs = list(filter(None,
                          executor.map(generate_report_config,
                                       remaining_files)))


print(f"{len(configs)} stocks selected...")

for config in configs:
    make_report(config)

