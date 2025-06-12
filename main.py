from src.data_analyze import merged_data_loader
from src.data_loader import RawData
from src.data_processing import ProcessedData


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
    analyze_data = merged_data_loader('data/processed/merged_data.csv')

    print("Analysis complete.")


def main():
    raw_data = collect_data()
    process_data(raw_data)
    results = analyze_data()



    

if __name__ == "__main__":
    main()

