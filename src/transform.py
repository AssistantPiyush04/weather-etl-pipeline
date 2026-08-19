import json
import os
import pandas as pd
from pathlib import Path

def transform_weather_data():

   raw_dir=Path("data/raw")
   raw_files= list(raw_dir.glob("weather_*.json"))
   latest_file=max(
   raw_files,
   key=lambda file: file.stat().st_mtime
)
   with open(latest_file,"r") as f:
    raw_data= json.load(f)

   current_data= raw_data["current"]

   temperature= current_data["temperature_2m"]
   humidity= current_data["relative_humidity_2m"]
   wind_speed= current_data["wind_speed_10m"]
   recorded_at= current_data["time"]

   city="jaipur"
   weather_record={
    "city":city,
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
   df["recorded_at"]=pd.to_datetime(df["recorded_at"])
   print(df)
   print(df.isnull().sum())
   print(df.dtypes)

   output_dir= "data/processed"

   os.makedirs(output_dir, exist_ok=True)
   output_file= f"{output_dir}/weather_data.csv"
   df.to_csv(output_file, index=False)
   print(f"Clean data saved to : {output_file}")

   return output_file

if __name__ == "__main__":
    transform_weather_data()

    


    