import pandas as pd
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def readCSV(path):
    return pd.read_csv(path)

def connect():
    url = f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@localhost:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    engine = create_engine(url)
    print("connected")
    return engine

def loadCities(engine, df):
    cities = df[["city", "latitude", "longitude", "admin_name", "population"]].drop_duplicates("city")

    sql = text("""
        INSERT INTO cities (city, latitude, longitude, admin_name, population)
        VALUES (:city, :latitude, :longitude, :admin_name, :population)
        ON CONFLICT (city) DO UPDATE SET
            latitude = EXCLUDED.latitude,
            longitude = EXCLUDED.longitude,
            admin_name = EXCLUDED.admin_name,
            population = EXCLUDED.population
    """)

    with engine.begin() as conn:
        for row in cities.itertuples():
            conn.execute(sql, {
                "city": row.city,
                "latitude": row.latitude,
                "longitude": row.longitude,
                "admin_name": row.admin_name,
                "population": row.population
            })

    print(f"loaded {len(cities)} cities")

def loadForecasts(engine, df):
    with engine.begin() as conn:
        cityMap = dict(conn.execute(text("SELECT city, city_id FROM cities")).fetchall())

        for row in df.itertuples():
            conn.execute(text("""
                INSERT INTO weather_forecast (
                    city_id, date, fetched_at,
                    temp_max, temp_min, precip, precip_prob,
                    wind_speed, wind_gusts, weather_code,
                    risk_score, temp_category, rain_category, wind_category
                )
                VALUES (
                    :city_id, :date, :fetched_at,
                    :temp_max, :temp_min, :precip, :precip_prob,
                    :wind_speed, :wind_gusts, :weather_code,
                    :risk_score, :temp_category, :rain_category, :wind_category
                )
                ON CONFLICT (city_id, date) DO UPDATE SET
                    fetched_at = EXCLUDED.fetched_at,
                    temp_max = EXCLUDED.temp_max,
                    temp_min = EXCLUDED.temp_min,
                    precip = EXCLUDED.precip,
                    precip_prob = EXCLUDED.precip_prob,
                    wind_speed = EXCLUDED.wind_speed,
                    wind_gusts = EXCLUDED.wind_gusts,
                    weather_code = EXCLUDED.weather_code,
                    risk_score = EXCLUDED.risk_score,
                    temp_category = EXCLUDED.temp_category,
                    rain_category = EXCLUDED.rain_category,
                    wind_category = EXCLUDED.wind_category
            """),
                {
                    "city_id": cityMap[row.city],
                    "date": row.time,
                    "fetched_at": row.fetched_at,
                    "temp_max": row.temperature_2m_max,
                    "temp_min": row.temperature_2m_min,
                    "precip": row.precipitation_sum,
                    "precip_prob": row.precipitation_probability_max,
                    "wind_speed": row.wind_speed_10m_max,
                    "wind_gusts": row.wind_gusts_10m_max,
                    "weather_code": row.weather_code,
                    "risk_score": row.risk_score,
                    "temp_category": row.temp_category,
                    "rain_category": row.rain_category,
                    "wind_category": row.wind_speed_category
                }
            )

    print(f"loaded {len(df)} forecasts")

if __name__ == "__main__":
    engine = connect()
    df = readCSV("gold/data.csv")
    loadCities(engine, df)
    loadForecasts(engine, df)