import matplotlib
import pandas

matplotlib.use("Agg")
import pathlib
import matplotlib.pyplot as plt

def generate_graph(x_lables,y_lables,title):
    main_folder = pathlib.Path("Div_Graphs")
    main_folder.mkdir(parents=True, exist_ok=True)

    plt.bar(x=x_lables,height=y_lables)
    plt.xlabel("Year")
    plt.ylabel("Dividend")
    plt.xticks(rotation=90)
    plt.title(f"{title}")

    plt.savefig(f"{main_folder.absolute()}/{title}.png")
    print(f"Graph saved for {title}.")
    plt.close()


def get_year(text):
    return str(text).split("-")[-1]

def normal_process_obtaining(data):
    allowed = '0123456789'
    temp1 = data.split(" ")
    for k in temp1:
        if bool(set(k) & set(allowed)):
            char_map = []
            letters = list(k)
            for g in letters:
                char_map.append(g.isdigit())
            first_index = char_map.index(True)
            last_index = len(char_map) - char_map[::-1].index(True)

            final_changing = "".join(letters[first_index:last_index])

            if final_changing.count(".") > 1:
                temp2 = []
                for i in letters:
                    if (i == '.' and "." not in temp2) or (i != '.'):
                        temp2.append(i)

                return float("".join(temp2))

            return float(final_changing)
    return 0

def remove_bonus(text):
    data = str(text).split("/")
    for i in data:
        if "dividend" in i:
            return i
    return 0


def extract_dividend_value(text):
    try:
        if "bonus" in text:
            temp1 = remove_bonus(text)
            return normal_process_obtaining(temp1)
        else:
            return normal_process_obtaining(str(text).replace("/"," ").replace("-"," "))
    except:
        return "problem 0"


for i in pathlib.Path("Dividends").iterdir():
    data_csv = pandas.read_csv(i.absolute())
    temp1 = data_csv[["PURPOSE","EX-DATE"]]

    if len(temp1)>0:

        print("=" * 60)
        print(i)

        dividend_data = {}
        format_code = ""
        for b in range(len(temp1)):
            temp2_dividend = str(temp1["PURPOSE"][b])
            year = get_year(temp1["EX-DATE"][b])
            if "%" not in temp2_dividend:
                temp3=extract_dividend_value(temp2_dividend.lower())
                print(f"{temp3} ~~~~ {year}")

                if year not in dividend_data.keys():
                    dividend_data[year]=temp3
                else:
                    dividend_data[year] = temp3 + dividend_data[year]

        generate_graph(list(dividend_data.keys()),
                       list(dividend_data.values()),i.name.replace(".csv",""))
