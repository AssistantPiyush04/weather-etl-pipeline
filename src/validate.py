import mysql.connector
import os

from dotenv import load_dotenv
from logger import logger

load_dotenv()


def validate_weather_data():

    logger.info("Data validation started")

    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    cursor = connection.cursor(dictionary=True)

    logger.info("Connected to MySQL successfully")

    cursor.execute("""
        SELECT *
        FROM weather_reports
        ORDER BY id DESC
    """)

    records = cursor.fetchall()

    # NULL validation
    null_records = 0

    for record in records:

        if (
            record["city"] is None
            or record["temperature"] is None
            or record["humidity"] is None
            or record["wind_speed"] is None
            or record["recorded_at"] is None
        ):
            null_records += 1

    if null_records == 0:
        print("NULL check: PASS")
        logger.info("NULL check passed")
    else:
        print(
            f"NULL check: FAIL - "
            f"{null_records} records contain NULL values"
        )
        logger.warning(
            f"NULL check failed - "
            f"{null_records} records contain NULL values"
        )

    print(f"Total records fetched: {len(records)}")
    logger.info(f"{len(records)} records fetched for validation")

    # Range validation
    invalid_humidity = 0
    invalid_wind_speed = 0
    invalid_temperature = 0

    for record in records:

        if record["humidity"] < 0 or record["humidity"] > 100:
            invalid_humidity += 1

        if record["wind_speed"] < 0:
            invalid_wind_speed += 1

        if (
            record["temperature"] < -50
            or record["temperature"] > 60
        ):
            invalid_temperature += 1

    # Humidity result
    if invalid_humidity == 0:
        print("Humidity check: PASS")
        logger.info("Humidity range check passed")
    else:
        print(
            f"Humidity check: FAIL - "
            f"{invalid_humidity} invalid records"
        )
        logger.warning(
            f"Humidity range check failed - "
            f"{invalid_humidity} invalid records"
        )

    # Wind speed result
    if invalid_wind_speed == 0:
        print("Wind speed check: PASS")
        logger.info("Wind speed range check passed")
    else:
        print(
            f"Wind speed check: FAIL - "
            f"{invalid_wind_speed} invalid records"
        )
        logger.warning(
            f"Wind speed range check failed - "
            f"{invalid_wind_speed} invalid records"
        )

    # Temperature result
    if invalid_temperature == 0:
        print("Temperature check: PASS")
        logger.info("Temperature range check passed")
    else:
        print(
            f"Temperature check: FAIL - "
            f"{invalid_temperature} invalid records"
        )
        logger.warning(
            f"Temperature range check failed - "
            f"{invalid_temperature} invalid records"
        )

    cursor.close()
    connection.close()


if __name__ == "__main__":
    validate_weather_data()