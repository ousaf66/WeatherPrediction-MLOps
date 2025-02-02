import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from math import sqrt
from statsmodels.tsa.arima.model import ARIMA
import mlflow
import mlflow.pyfunc
import mlflow.statsmodels

def load_data(csv_path="prepared_data.csv"):
    df = pd.read_csv(csv_path, parse_dates=["timestamp"])
    df.set_index("timestamp", inplace=True)
    return df["temp"]

def train_arima(series, order=(1,1,1)):
    # Fit ARIMA model
    model = ARIMA(series, order=order)
    model_fit = model.fit()
    return model_fit

def evaluate(model_fit, train_size=0.8):
    # Split train/val
    y = model_fit.model.endog
    n_train = int(len(y) * train_size)
    train, val = y[:n_train], y[n_train:]
    # Forecast on validation set length
    forecast = model_fit.forecast(steps=len(val))
    rmse = sqrt(mean_squared_error(val, forecast))
    return rmse

def main():
    # Start an MLflow run
    with mlflow.start_run():
        # Load the data
        data = load_data()
        order = (1, 1, 1)  # Example ARIMA parameters
        
        # Log model parameters
        mlflow.log_param("order_p", order[0])
        mlflow.log_param("order_d", order[1])
        mlflow.log_param("order_q", order[2])
        
        # Train the model
        model_fit = train_arima(data, order=order)
        
        # Evaluate the model
        rmse = evaluate(model_fit)
        
        # Log the RMSE metric
        mlflow.log_metric("rmse", rmse)
        
        # Save the model with MLflow
        mlflow.statsmodels.log_model(
            statsmodels_model=model_fit,
            artifact_path="arima_model",
            registered_model_name="ARIMA_Model"
        )
        
        print(f"Model trained and logged with RMSE: {rmse}")

if __name__ == "__main__":
    # Set MLflow experiment
    mlflow.set_experiment("ARIMA_Model_Experiment")
    main()
