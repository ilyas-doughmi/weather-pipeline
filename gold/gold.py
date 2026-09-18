import pandas as pd

def readCSV(path):
    return pd.read_csv(path)

def tempCategory(maxTemp):
    if maxTemp < 0:
        return "froid"
    elif maxTemp < 15:
        return "frais"
    elif maxTemp < 30:
        return "doux"
    elif maxTemp < 40:
        return "chaud"
    else:
        return "extreme"

def rainCategory(rain):
    if rain == 0 :
        return "sec"
    elif rain < 5 : 
        return "legere"
    elif rain < 20:
        return  "moderee"
    else:
        return "forte"

def windSpeedCategory(windSpeed):
    if windSpeed < 20:
        return "calme"
    elif windSpeed < 40:
        return "modere"
    elif windSpeed < 60:
        return "fort"
    else:
        return "violent"


def riskScore(row):
    score = 0

    rain = row["precipitation_sum"]
    if rain >= 20:
        score += 30
    elif rain >= 5:
        score += 10
    elif rain > 0:
        score += 5

    windGust = row["wind_gusts_10m_max"]
    if windGust >= 80:
        score += 20
    elif windGust >= 50:
        score += 12
    elif windGust >= 30:
        score += 4  

    maxTemp = row["temperature_2m_max"]
    if maxTemp >= 45:
        score += 15
    elif maxTemp >= 38:
        score += 10
    elif maxTemp <= 0:
        score += 8

    rainChance = row["precipitation_probability_max"]
    if rainChance >= 70:
        score += 10
    elif rainChance >= 40:
        score += 5

    windSpeed = row["wind_speed_10m_max"]
    if windSpeed >= 60:
        score += 25
    elif windSpeed >= 40:
        score += 15
    elif windSpeed >= 20:
        score += 5

    return min(score,100)

def buildGold():
    df = readCSV("silver/data.csv")
    df["temp_category"] = df["temperature_2m_max"].apply(tempCategory)
    df["rain_category"] = df["precipitation_sum"].apply(rainCategory)
    df["wind_speed_category"] = df["wind_speed_10m_max"].apply(windSpeedCategory)
    df["risk_score"] = df.apply(riskScore, axis=1)
    df.to_csv("gold/data.csv", index=False)
    return df

if __name__ == "__main__":
    buildGold()