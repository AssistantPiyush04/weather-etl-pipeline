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

   df=pd.read_csv(csv_file)
   print(df)

   cursor= connection.cursor()

   insert_query= """
   insert ignore into weather_reports 
   (city,temperature,humidity,wind_speed,recorded_at)
   values(%s, %s, %s, %s, %s)
   """

   inserted_count=0
   duplicate_count=0

   for _, row in df.iterrows():
      values=(
         row["city"],
         row["temperature"],
         row["humidity"],
         row["wind_speed"],
         row["recorded_at"]
      )
      cursor.execute(insert_query, values)

      if cursor.rowcount==1:
         inserted_count+=1
      else:
         duplicate_count+=1

   connection.commit()
   cursor.close()
   connection.close()

   print(f"Inserted_count: {inserted_count}")
   print(f"Duplicate_count: {duplicate_count}")
   print(f"Data loaded into MYSQL database successfully")

   return inserted_count, duplicate_count

if __name__ == '__main__':
   load_weather_data("data/processed/weather_data.csv")
