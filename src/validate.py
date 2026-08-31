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

    validation_passed = True

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
        validation_passed = False

    print(f"Total records fetched: {len(records)}")

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

    # Humidity
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
        validation_passed = False

    # Wind speed
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
        validation_passed = False

    # Temperature
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
        validation_passed = False

    # Duplicate validation
    cursor.execute("""
        SELECT city, recorded_at, COUNT(*) AS duplicate_count
        FROM weather_reports
        GROUP BY city, recorded_at
        HAVING COUNT(*) > 1
    """)

    duplicate_records = cursor.fetchall()

    if len(duplicate_records) == 0:
        print("Duplicate check: PASS")
        logger.info("Duplicate check passed")
    else:
        print(
            f"Duplicate check: FAIL - "
            f"{len(duplicate_records)} duplicate groups found"
        )
        logger.warning(
            f"Duplicate check failed - "
            f"{len(duplicate_records)} duplicate groups found"
        )
        validation_passed = False

    # Final report
    print("\n=============================")
    print("     DATA QUALITY REPORT")
    print("=============================")
    print(f"Total records       : {len(records)}")
    print(
        f"NULL check          : "
        f"{'PASS' if null_records == 0 else 'FAIL'}"
    )
    print(
        f"Humidity check      : "
        f"{'PASS' if invalid_humidity == 0 else 'FAIL'}"
    )
    print(
        f"Wind speed check    : "
        f"{'PASS' if invalid_wind_speed == 0 else 'FAIL'}"
    )
    print(
        f"Temperature check   : "
        f"{'PASS' if invalid_temperature == 0 else 'FAIL'}"
    )
    print(
        f"Duplicate check     : "
        f"{'PASS' if len(duplicate_records) == 0 else 'FAIL'}"
    )
    print("-----------------------------")

    if validation_passed:
        print("Overall status      : PASS")
        logger.info("Overall data quality validation passed")
    else:
        print("Overall status      : FAIL")
        logger.warning("Overall data quality validation failed")

    print("=============================")

    cursor.close()
    connection.close()

    return validation_passed

if __name__ == "__main__":
    validate_weather_data()