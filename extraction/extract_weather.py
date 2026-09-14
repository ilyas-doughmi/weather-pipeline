import pandas as pd


def readCSV(path):
    df = pd.read_csv(path,encoding="utf-8")
    return df[["city","lat","lon"]]

if __name__ == "__main__":
    print(readCSV("data/ma-cities.csv"))
