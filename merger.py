import pathlib,pandas

data_merged = {f'{i.stem}':i for i in pathlib.Path("Merged").iterdir()}
remaining_data = {f'{i.stem}':i for i in pathlib.Path("History").iterdir()}

result = list(set(remaining_data.keys()) - set(data_merged.keys()))

remaining_files = []

for i in result:
    try:
        remaining_files.append(remaining_data[i])
    except Exception as e:
        print(e)

ratio = len(remaining_files)/len(remaining_data)
print(f"Remaining {len(remaining_files)} | {round(ratio*100,3)}%")

for i in remaining_files:
    dfs=[]
    for k in pathlib.Path(i.absolute()).iterdir():
        df = pandas.read_csv(k)[::-1]
        dfs.append(df)

    if len(dfs)>0:
        merged_data = pandas.concat(dfs, ignore_index=True)
        print("=" * 50)
        print(i.name)
        main_folder = pathlib.Path("Merged")
        main_folder.mkdir(parents=True, exist_ok=True)
        merged_data.to_csv(f"Merged/{str(i.stem).replace("_completed","")}.csv",index=False)

