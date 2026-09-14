import pandas as pd
import json
import requests as req
from datetime import datetime
import os

def readCSV(path):
    df = pd.read_csv(path,encoding="utf-8")
    return df[["city","lat","lon"]]

def build_url(lat,lon):
    baseUrl = "https://api.open-meteo.com/v1/forecast"
    return baseUrl + f"?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,wind_speed_10m_max,wind_gusts_10m_max,weather_code&timezone=auto&forecast_days=3"

def main():
    df = readCSV("data/ma-cities.csv")
    for data in df.itertuples():
        print(f"extracting {data.city}....")
        lat,lon = data.lat,data.lon
        url = build_url(lat,lon)
        response = req.get(url).json()

        payload = {
            "city": data.city,
            "lat" : data.lat,
            "lon" : data.lon,
            "timestamp" : datetime.now().isoformat(),
            "response" : response
        }

        try: 
            with open(f"bronze/{data.city}.json", "w") as f:
                print(f"creating json file for  {data.city}....")
                json.dump(payload,f)
        except FileNotFoundError:
            print("folder not exists\nCreating new one")
            os.makedirs("bronze/")
        

        print(f"Done {data.city}")

if __name__ == "__main__":  
    main()