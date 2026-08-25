import mysql.connector
import os

from dotenv import load_dotenv
from logger import logger

load_dotenv()

def validate_weather_data():
    logger.info("Data validation started")

    connection= mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    );

    cursor=connection.cursor(dictionary=True)

    logger.info("connected to mysql succedfully")

    cursor.execute("""
      select * 
      from weather_reports
      order by id desc
    """)

    records=cursor.fetchall()

    null_records=0

    for record in records:
        if(
            record["city"] is None 
           or record["temperature"] is None
           or record["humidity"] is None
           or record["wind_speed"] is None
           or record["recorded_at"] is None

        ):
           null_records+=1
        
    if null_records == 0:
        print("Null: check pass")
        logger.info("Null checked passes")

    else:
        print(f"Null check Fail- {null_records} records contain null values")
        logger.warning(f"Null checked failed- {null_records} records contain null values")

    print(f"Total records fetched: {len(records)}")
    logger.info(f"{len(records)} records fetched for validation")

    cursor.close()
    connection.close()

if __name__ == "__main__":
    validate_weather_data()
