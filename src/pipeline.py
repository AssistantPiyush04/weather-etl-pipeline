from extract import fetch_weather_data, save_raw_data, cleanup_old_files
from transform import transform_weather_data
from load import load_weather_data
from validate import validate_weather_data
from logger import logger
import sys


def run_pipeline():

    extract_status = "NOT RUN"
    transform_status = "NOT RUN"
    load_status = "NOT RUN"
    validation_status = "NOT RUN"

    logger.info("ETL Pipeline started")

    try:

        # EXTRACT
        data = fetch_weather_data() 
        save_raw_data(data)
        cleanup_old_files()
        extract_status = "SUCCESS"

        # TRANSFORM
        csv_file = transform_weather_data()
        transform_status = "SUCCESS"

        # LOAD
        inserted_count, duplicate_count = load_weather_data(csv_file)
        load_status = "SUCCESS"

        # VALIDATION
        validation_result = validate_weather_data()

        if validation_result:
            validation_status = "PASS"
        else:
            validation_status = "FAIL"
            raise ValueError("Data quality validation failed")

        # SUCCESS SUMMARY
        print("\n=============================")
        print("       ETL PIPELINE SUMMARY")
        print("=============================")
        print(f"Extract       : {extract_status}")
        print(f"Transform     : {transform_status}")
        print(f"Load          : {load_status}")
        print(f"Validation    : {validation_status}")
        print("-------------------------------")
        print("Pipeline       : Success")
        print("================================")

        logger.info("ETL Pipeline completed successfully")

        return True

    except Exception as error:

        logger.error(f"Pipeline failed: {error}")

        print("\n=============================")
        print("       ETL PIPELINE SUMMARY")
        print("=============================")
        print(f"Extract       : {extract_status}")
        print(f"Transform     : {transform_status}")
        print(f"Load          : {load_status}")
        print(f"Validation    : {validation_status}")
        print(f"Duplicates    : {duplicate_count}")
        print(f"Validation Result: {validation_result}")
        print("-------------------------------")
        print("Pipeline       : Failed")
        print("================================")

        sys.exit(1)


if __name__ == "__main__":
    run_pipeline()
