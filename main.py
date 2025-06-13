
from src.data_loader import RawData
from src.data_processing import ProcessedData
from src.db_loader import EnergyDataDB
from src.data_prediction import EnergyPredictor, predicted_last_week_data
from src.data_analyze import show_month_data, show_day_data, show_hourly_winter_data, show_hourly_summer_data, show_hourly_winter_workday_data, show_hourly_summer_workday_data
import pandas as pd
import matplotlib.pyplot as plt


def collect_data():
    """
    Collects data from various sources and returns a dictionary containing the data.
    """
    print("\nStarting data processing...")
    raw_data = RawData()
    print("Raw data collected successfully.\n")

    return raw_data

def process_data(raw_data):
    """
    Collects and processes data, then returns the processed data object.
    """
    print("Processing raw data...")
    processed_data = ProcessedData(raw_data)
    print("Raw data processed successfully.\n")

    return processed_data



def analyze_data():
    """
    Analyzes the processed data and returns the analysis results.
    """
    print("Analyzing processed data...")
    database = EnergyDataDB()

    show_month_data(database)
    show_day_data(database)
    show_hourly_summer_data(database)
    show_hourly_winter_data(database)
    show_hourly_winter_workday_data(database)
    show_hourly_summer_workday_data(database)
    return database



def predicted_data():
    
    print("Creating prediction model data...")
    predictor = EnergyPredictor(db_path="data/database.db")
    predictor.show_model_info()
    print("Training the model done")

    print("predicting last week data...")
    predicted_last_week_data()
    print("Predicted data for last week created successfully.\n")
    


def main():
    raw_data = collect_data()
    process_data(raw_data)
    analyze_data()
    predicted_data()


if __name__ == "__main__":
    main()

