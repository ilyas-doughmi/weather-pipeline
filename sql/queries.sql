SELECT city, date, temp_max
FROM weather_forecast
JOIN cities ON weather_forecast.city_id = cities.city_id
ORDER BY temp_max DESC
LIMIT 5;

SELECT city, date, precip
FROM weather_forecast
JOIN cities ON weather_forecast.city_id = cities.city_id
ORDER BY precip DESC
LIMIT 5;

SELECT city, AVG(risk_score) AS moyenne_risque
FROM weather_forecast
JOIN cities ON weather_forecast.city_id = cities.city_id
GROUP BY city
ORDER BY moyenne_risque DESC
LIMIT 5;

SELECT date, AVG(risk_score) AS moyenne_risque, MAX(risk_score) AS max_risque
FROM weather_forecast
GROUP BY date
ORDER BY moyenne_risque DESC;

SELECT city, MAX(risk_score) AS max_risque
FROM weather_forecast
JOIN cities ON weather_forecast.city_id = cities.city_id
GROUP BY city
ORDER BY max_risque DESC
LIMIT 15;