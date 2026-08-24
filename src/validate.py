import mysql.connector
from logger import logger

def validate_weather_data():
    logger.info("Data validation started")

    connection= mysql.connector.connect(
        host="localhost",
        user="root",
        password="Piyush@2004sql",
        database="weather_etl"
    );

    cursor=connection.cursor(dictionary=True)

    cursor.execute("""
      select * 
      from weather_reports
      order by id desc
    """)

    records=cursor.fetchall()

    logger.info(f"{len(records)} records fetched for validation")

    cursor.close()
    connection.close()

if __name__ == "__main__":
    validate_weather_data()
