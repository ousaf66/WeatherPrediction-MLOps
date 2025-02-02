import os
import json
import pandas as pd
from datetime import datetime

DATA_DIR = "data/"
OUTPUT_CSV = "prepared_data.csv"

def load_data(data_dir=DATA_DIR):
    # Load all JSON files and concatenate into a single DataFrame
    records = []
    for filename in os.listdir(data_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(data_dir, filename)
            with open(filepath, 'r') as f:
                data = json.load(f)
                # Example: Extract timestamp and temperature from weather data
                # Adapt this based on your actual data structure.
                # Suppose `data` has `list` of forecasts with `dt` (timestamp) and `main.temp`
                if "list" in data:
                    for entry in data["list"]:
                        dt = datetime.utcfromtimestamp(entry["dt"])
                        temp = entry["main"]["temp"]
                        records.append({"timestamp": dt, "temp": temp})
    return pd.DataFrame(records)

def preprocess(df):
    # Sort by time and drop duplicates
    df = df.drop_duplicates("timestamp").sort_values("timestamp")
    # Handle missing values if any (e.g., forward fill)
    df = df.fillna(method='ffill')
    return df

def main():
    df = load_data()
    df = preprocess(df)
    # Save prepared data
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Prepared data saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
