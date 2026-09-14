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
    os.makedirs("bronze", exist_ok=True)
    df = readCSV("data/ma-cities.csv")
    for data in df.itertuples():
        if " " in data.city:
            city = data.city.replace(" ","_").lower()
        else:
            city = data.city.lower()
        print(f"extracting {data.city}....")
        lat,lon = data.lat,data.lon
        url = build_url(lat,lon)
        response = None
        for tries in range(1,5):
            try:    
                response = req.get(url, timeout=10)
                response.raise_for_status()
                break
            except req.exceptions.RequestException as e :
                print(f"failed : {tries}/4 : failed:{e}")
                if tries == 4:
                    print(f"All retries failed for {data.city}")
                    with open(f"bronze/{city}-failed.json","w", encoding="utf-8") as f:
                        json.dump(str(e),f)
        if response is None:
            print(f"Skipping {data.city}")
            continue
        payload = {
            "city": data.city,
            "lat" : data.lat,
            "lon" : data.lon,
            "fetched_at" : datetime.now().isoformat(),
            "response" : response.json()
        }
        with open(f"bronze/{city}.json", "w", encoding="utf-8") as f:
            print(f"creating json file for  {data.city}....")
            json.dump(payload, f, ensure_ascii=False, indent=2)     
        print(f"Done {data.city}")

    print("Done...")
if __name__ == "__main__":  
    main()