import requests
from pathlib import Path
import json
from datetime import datetime
import time
from logger import logger
    
def fetch_weather_data():
    url= "https://api.open-meteo.com/v1/forecast"

    params={
        "latitude": 26.9124,
        "longitude":75.7873,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
        "timezone": "Asia/Kolkata"
    }

    for attempt in range(3):
        try:
            response=requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            logger.info("Weather data fetched successfully")
            return response.json()
        except requests.exceptions.RequestException as error:
            print(f"Attempt: {attempt+1} failed: {error}") 
            logger.warning(f"Attempt: {attempt+1} failed: {error}")  

            if attempt<2:
                print("Retrying...")
                time.sleep(2)
            else:
                raise

def save_raw_data(data):
    raw_dir= Path("data/raw")
    raw_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    file_Path= raw_dir / f"weather_{timestamp}.json"

    with open(file_Path, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Raw data saved to: {file_Path}")
    logger.info(f"Raw data saved to: {file_Path}")


def cleanup_old_files(keep=10):
    raw_dir=Path("data/raw")

    raw_files=list(raw_dir.glob("weather_*.json"))
    raw_files.sort(key=lambda file: file.stat().st_mtime, reverse=True)

    for old_file in raw_files[keep:]:
        old_file.unlink()
        logger.info(f"Deleted old raw file: {old_file}")


if __name__ == "__main__":
    data= fetch_weather_data()
    save_raw_data(data)
    cleanup_old_files()
    extract_status= "SUCCESS"