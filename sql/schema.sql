CREATE TABLE cities (
    city_id    SERIAL PRIMARY KEY,
    city       VARCHAR(50) UNIQUE NOT NULL,
    latitude   NUMERIC,
    longitude  NUMERIC,
    admin_name VARCHAR(50),
    population INT
);

CREATE TABLE weather_forecast (
    forecast_id SERIAL PRIMARY KEY,
    city_id     INT REFERENCES cities(city_id),
    date        DATE,
    fetched_at  TIMESTAMP,
    temp_max    NUMERIC,
    temp_min    NUMERIC,
    precip      NUMERIC,
    precip_prob INT,
    wind_speed  NUMERIC,
    wind_gusts  NUMERIC,
    weather_code INT,
    risk_score  INT,
    temp_category VARCHAR(20),
    rain_category VARCHAR(20),
    wind_category VARCHAR(20),
    UNIQUE (city_id, date)
);