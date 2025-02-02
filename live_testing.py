import time
import requests
import pandas as pd
from datetime import datetime, timedelta

# Configuration
API_URL = "http://localhost:8000/predict"
LIVE_DATA_API = "https://api.openweathermap.org/data/2.5/forecast"
API_KEY = 'd330d53c8518627cb2f9743604a51c86'  # Replace with your API key
LOCATION = {"lat": 40.7128, "lon": -74.0060}  # Example: New York City

def fetch_live_data():
    """Fetch live air pollution data from OpenWeatherMap API."""
    params = {
        "lat": LOCATION["lat"],
        "lon": LOCATION["lon"],
        "appid": API_KEY
    }
    response = requests.get(LIVE_DATA_API, params=params)
    if response.status_code == 200:
        data = response.json()
        # Extract relevant data (e.g., PM2.5 concentration)
        pm25 = data["list"][0]["components"]["pm2_5"]
        timestamp = datetime.now()
        return {"timestamp": timestamp, "pm2_5": pm25}
    else:
        print(f"Error fetching live data: {response.status_code}")
        return None

def send_prediction_request(steps):
    """Send prediction request to FastAPI app."""
    response = requests.post(API_URL, json={"steps": steps})
    if response.status_code == 200:
        return response.json()["forecast"]
    else:
        print(f"Error during prediction: {response.status_code}")
        return None

def main():
    while True:
        # Fetch live data
        live_data = fetch_live_data()
        if live_data:
            print(f"Live Data: {live_data}")
        
        # Send prediction request
        forecast = send_prediction_request(steps=5)
        if forecast:
            print(f"Forecast: {forecast}")
        
        # Wait for next iteration
        time.sleep(3600)  # Run every hour

if __name__ == "__main__":
    main()
