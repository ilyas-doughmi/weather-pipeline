import pandas as pd
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def readCSV(path):
    return pd.read_csv(path)

def connect():
    conn = psycopg2.connect(
        host="localhost",
        port=os.getenv("POSTGRES_PORT"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        dbname=os.getenv("POSTGRES_DB")
    )
    print("connected")
    return conn

def loadCities(conn, df):
    cities = df[["city", "latitude", "longitude", "admin_name", "population"]].drop_duplicates("city")
    cur = conn.cursor()

    for row in cities.itertuples():
        sql = "INSERT INTO cities (city, latitude, longitude, admin_name, population) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (city) DO UPDATE SET latitude = EXCLUDED.latitude, longitude = EXCLUDED.longitude, admin_name = EXCLUDED.admin_name, population = EXCLUDED.population"
        cur.execute(sql, (row.city, row.latitude, row.longitude, row.admin_name, row.population))

    conn.commit()
    cur.close()
    print(f"loaded {len(cities)} cities")

def loadForecasts(conn, df):
    cur = conn.cursor()
    cur.execute("SELECT city, city_id FROM cities")
    cityMap = dict(cur.fetchall())

    for row in df.itertuples():
        sql = "INSERT INTO weather_forecast (city_id, date, fetched_at, temp_max, temp_min, precip, precip_prob, wind_speed, wind_gusts, weather_code, risk_score, temp_category, rain_category, wind_category) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (city_id, date) DO UPDATE SET fetched_at = EXCLUDED.fetched_at, temp_max = EXCLUDED.temp_max, temp_min = EXCLUDED.temp_min, precip = EXCLUDED.precip, precip_prob = EXCLUDED.precip_prob, wind_speed = EXCLUDED.wind_speed, wind_gusts = EXCLUDED.wind_gusts, weather_code = EXCLUDED.weather_code, risk_score = EXCLUDED.risk_score, temp_category = EXCLUDED.temp_category, rain_category = EXCLUDED.rain_category, wind_category = EXCLUDED.wind_category"
        cur.execute(sql, (cityMap[row.city], row.time, row.fetched_at, row.temperature_2m_max, row.temperature_2m_min, row.precipitation_sum, row.precipitation_probability_max, row.wind_speed_10m_max, row.wind_gusts_10m_max, row.weather_code, row.risk_score, row.temp_category, row.rain_category, row.wind_speed_category))

    conn.commit()
    cur.close()
    print(f"loaded {len(df)} forecasts")

if __name__ == "__main__":
    conn = connect()
    df = readCSV("gold/data.csv")
    loadCities(conn, df)
    loadForecasts(conn, df)
    conn.close()