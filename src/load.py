import os
from dotenv import load_dotenv
import pandas as pd
import mysql.connector


load_dotenv()

def load_weather_data(csv_file):
   connection= mysql.connector.connect(
      host= os.getenv("DB_HOST"),
      user= os.getenv("DB_USER"),
      password=os.getenv("DB_PASSWORD"),
      database=os.getenv("DB_NAME")
)

   print("Mysql connection is succesfull")

   csv_file= "data/processed/weather_data.csv"
   df=pd.read_csv(csv_file)
   print(df)

   cursor= connection.cursor()

   insert_query= """
   insert ignore into weather_reports 
   (city,temperature,humidity,wind_speed,recorded_at)
   values(%s, %s, %s, %s, %s)
   """

   for _, row in df.iterrows():
      values=(
         row["city"],
         row["temperature"],
         row["humidity"],
         row["wind_speed"],
         row["recorded_at"]
      )
      cursor.execute(insert_query, values)

   connection.commit()
   cursor.close()
   connection.close()

   print("Weather data loded succesfully in mysql")

if __name__ == '__main__':
   load_weather_data("data/processed/weather_data.csv")
