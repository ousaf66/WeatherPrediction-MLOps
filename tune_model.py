import pandas as pd
import numpy as np
from math import sqrt
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.arima.model import ARIMA
import mlflow
import mlflow.statsmodels

def load_data(csv_path="prepared_data.csv"):
    df = pd.read_csv(csv_path, parse_dates=["timestamp"])
    df.set_index("timestamp", inplace=True)
    df.index = pd.DatetimeIndex(df.index, freq='3H')  # Set to 3-hour frequency if that matches your data collection interval
    return df["temp"]

def evaluate_arima(series, order):
    n_train = int(len(series) * 0.8)
    train, val = series[:n_train], series[n_train:]
    model = ARIMA(train, order=order)
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=len(val))
    rmse = sqrt(mean_squared_error(val, forecast))
    return rmse, model_fit

def main():
    # Start an MLflow experiment
    mlflow.set_experiment("ARIMA_Evaluation_Experiment")
    
    with mlflow.start_run():
        data = load_data()
        orders = [(1, 1, 1), (2, 1, 2), (3, 1, 3)]
        best_rmse = float("inf")
        best_order = None
        best_model = None

        for order in orders:
            rmse, model_fit = evaluate_arima(data, order)
            
            # Log RMSE and ARIMA order for each model
            mlflow.log_param(f"order_p_{order}", order[0])
            mlflow.log_param(f"order_d_{order}", order[1])
            mlflow.log_param(f"order_q_{order}", order[2])
            mlflow.log_metric(f"RMSE_order_{order}", rmse)
            
            print(f"Tested ARIMA{order} -> RMSE: {rmse}")

            if rmse < best_rmse:
                best_rmse = rmse
                best_order = order
                best_model = model_fit

        # Log the best model details
        mlflow.log_metric("Best_RMSE", best_rmse)
        mlflow.log_param("Best_Order", best_order)

        # Save the best model with MLflow
        mlflow.statsmodels.log_model(
            statsmodels_model=best_model,
            artifact_path="best_arima_model",
            registered_model_name="Best_ARIMA_Model"
        )
        
        # Optionally save locally
        best_model.save("best_model.pkl")
        
        print(f"Best order: {best_order} with RMSE: {best_rmse}")

if __name__ == "__main__":
    main()
