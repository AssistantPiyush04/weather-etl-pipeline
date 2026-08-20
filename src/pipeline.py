from extract import fetch_weather_data, save_raw_data
from transform import transform_weather_data
from load import load_weather_data
from logger import logger


def run_pipeline():
    logger.info("ETL Pipeline started")

    try:
     data= fetch_weather_data()
     save_raw_data(data)
     csv_file= transform_weather_data()
     load_weather_data(csv_file)

     logger.info("ETL Pipeline compeleted succesfully")

    except Exception as error:
       logger.error(f"Pipeline failed {error}")
       raise

if __name__ == "__main__":
    run_pipeline()
