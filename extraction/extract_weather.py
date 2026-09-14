import pandas as pd

def readCSV(path):
    df = pd.read_csv(path,encoding="utf-8")
    return df[["city","lat","lon"]]

def build_url(lat,lon):
    baseUrl = "https://api.open-meteo.com/v1/forecast"
    return baseUrl + f"?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,wind_speed_10m_max,wind_gusts_10m_max,weather_code&timezone=auto&forecast_days=3"

if __name__ == "__main__":  
    print(build_url(52.52,13.41))