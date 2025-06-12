from src.data_colector import CalendarData, SunshineData, TemperatureData, WindData
from src.data_loader import RawData
from src.data_processing import ProcessedData


def colect_data():
    """
    Collects data from various sources and returns a dictionary containing the data.
    """
    raw_data = RawData()

    return raw_data


def main():
    print("\nStarting data processing...")
    raw_data = colect_data()
    print("Raw data collected successfully.\n")

    print("Processing raw data...")
    processing_data = ProcessedData(raw_data)
    print("Raw data processed successfully.\n")

    

if __name__ == "__main__":
    main()

