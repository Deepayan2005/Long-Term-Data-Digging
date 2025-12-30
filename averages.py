import pathlib
from concurrent.futures import ThreadPoolExecutor

import matplotlib
import matplotlib.pyplot as plt
import pandas

matplotlib.use("Agg")


def generate_graph(x_lables,y_lables,title):
    main_folder = pathlib.Path("Returns Graphs")
    main_folder.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(9,8))
    plt.plot(x_lables,y_lables)
    plt.xlabel("Year")
    plt.ylabel("Prices")
    plt.xticks(rotation=90)
    plt.title(f"{title}")
    path = f"{main_folder.absolute()}/{title}.png"
    plt.savefig(path)
    print(f"Graph saved for {title}.")
    plt.close()


def average(file : pathlib.Path):

    df = pandas.read_csv(file.absolute())
    df['close '] = df['close '].astype(str).str.replace(',', '').str.replace('-', '0.0').astype(float)
    df['date'] = pandas.to_datetime(df['Date '], format='mixed')
    df['year'] = df['date'].dt.year
    result = df.groupby('year')['close '].mean().reset_index().rename(columns={'close ': 'average'})
    result['change%'] = result['average'].pct_change() * 100

    result.to_csv(f"Averages/{file.name.replace('_completed','')}",index=False)

    print("~" * 60)
    print(f"average for {file.stem} is generated.")

data_merged = {f'{i.stem.replace("_completed","")}':i for i in pathlib.Path("Merged").iterdir()}
average_data = {f'{i.stem}':i for i in pathlib.Path("Averages").iterdir()}

result = list(set(data_merged.keys()) - set(average_data.keys()))

remaining_files = [data_merged[i] for i in result]

print(f"Remaining {len(remaining_files)} files....")
with ThreadPoolExecutor(max_workers=25) as executor:
    executor.map(average, remaining_files)


