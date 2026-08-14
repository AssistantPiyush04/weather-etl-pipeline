import json
import pandas as pd

#def transform_weather_data(raw_data):

with open("data/raw/weather_2026-08-13_14-04-04.json", "r") as f:
    raw_data= json.load(f)
    current_data= raw_data["current"]

    temperature= current_data["temperature_2m"]
    humidity= current_data["relative_humidity_2m"]
    wind_speed= current_data["wind_speed_10m"]
    recorded_at= current_data["time"]

    weather_record={
        "temperature":temperature,
        "humidity":humidity,
        "wind_speed": wind_speed,
        "recorded_at":recorded_at
    }

    print(temperature)
    print(humidity)
    print(wind_speed)
    print(recorded_at)
    print(weather_record)

    df=pd.DataFrame([weather_record])

    output_dir= "data/processed"

    import os
    os.makedirs(output_dir, exist_ok=True)
    output_file= f"{output_dir}/weather_data.csv"
    df.to_csv(output_file, index=False)
    print(f"Clean data saved to : {output_file}")


    df["recorded_at"]=pd.to_datetime(df["recorded_at"])
    print(df)
    print(df.isnull().sum())
    print(df.dtypes)

    


    