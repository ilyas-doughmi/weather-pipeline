import os
import json
import pandas as pd

def bronzedata(path):
    jsonFile = []
    for file in os.listdir(path):
        if ".json" in file and "-failed.json" not in file:
            jsonFile.append(file)

    return jsonFile

def buildrows(path,files):
    frames = []

    for file in files:
        with open(f"{path}/{file}","r") as f:
            data =json.load(f)
            daily = data["response"]["daily"]
            df = pd.DataFrame([daily])
            df["city"] = data["city"]
            df["latitude"] = data["lat"]
            df["longitude"] = data["lon"]
            df["fetched_at"] = data["fetched_at"]
            frames.append(df) 
    combine = pd.concat(frames,ignore_index=False)
    combine = combine.explode(["time","temperature_2m_max","temperature_2m_min","precipitation_sum","precipitation_probability_max","wind_speed_10m_max","wind_gusts_10m_max","weather_code"])
    combine.to_csv("silver/data.csv", index=True)

if __name__ ==  "__main__":
   print( buildrows("bronze",bronzedata("bronze")))