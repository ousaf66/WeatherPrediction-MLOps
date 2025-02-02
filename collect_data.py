import requests
import json
import os
from datetime import datetime

# Hardcoded OpenWeatherMap API Key (Replace with your actual API key)
API_KEY_OPENWEATHER = 'd330d53c8518627cb2f9743604a51c86'

# 5 Day / 3 Hour Forecast Endpoint
FORECAST_URL = 'https://api.openweathermap.org/data/2.5/forecast'

# Coordinates for the location of interest
LAT = 44.34
LON = 10.99

# Data Directory
DATA_DIR = "data/"

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

def fetch_forecast_data(lat=LAT, lon=LON):
    params = {
        'lat': lat,
        'lon': lon,
        'appid': API_KEY_OPENWEATHER,
        # Optional: Add 'units' for metric, imperial, or default units.
        # 'units': 'metric'
    }
    response = requests.get(FORECAST_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Forecast API Error: {response.status_code} - {response.text}")
        return None

def save_data(data, filename):
    with open(os.path.join(DATA_DIR, filename), 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {filename}")

def main():
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # Fetch Forecast Data
    forecast_data = fetch_forecast_data()
    if forecast_data:
        forecast_filename = f"forecast_{timestamp}.json"
        save_data(forecast_data, forecast_filename)

if __name__ == "__main__":
    main()
