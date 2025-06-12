
from src.data_loader import RawData
from src.data_processing import ProcessedData
from src.db_loader import EnergyDataDB


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
    results = database.get_average_consumption_per_year()
    print(f"Results for year 2023: {results}")
    print("Analysis complete.")


def main():
    raw_data = collect_data()
    process_data(raw_data)
    analyze_data()


if __name__ == "__main__":
    main()

