# 1. Import knihoven
import pandas as pd
import matplotlib.pyplot as plt

# 2. Načtení a příprava dat
def consumption_data_loader(file_path: str) -> pd.DataFrame:
    """
    Loads data from a CSV file into a pandas DataFrame, parsing the 'Date' column as datetime and setting it as the index.
    Args:
        file_path (str): The path to the CSV file to load.
    Returns:
        pd.DataFrame: The loaded data with 'Date' as the index.
    Raises:
        SystemExit: If the file is not found or if the 'Date' column is missing.
        ValueError: For other value errors encountered during loading.
    Notes:
        - The CSV file is expected to use ';' as the separator.
        - The 'Date' column must be present in the file in format 'DD.MM.YYYY HH:MM'.
    """
    
    try:
        load_data = pd.read_csv(file_path, sep=';', parse_dates=['Date'], dayfirst=True)
        load_data.set_index('Date', inplace=True)
        print(f"Data successfully loaded from {file_path}.")

    except FileNotFoundError:
        print(f"File {file_path} not found.")
        exit(1)
    except ValueError as e:
        if "Missing column provided to 'parse_dates': 'Date'" in str(e):
            print("Column 'Date' not found in the file.")
            exit(1)
        else:
            raise

    check_raw_data(load_data)

    return load_data

def check_raw_data(df: pd.DataFrame)-> None:

    print("\n--- Raw Data Check ---")
    print("Shape:", df.shape)
    print("Missing values per column:\n", df.isnull().sum())
    print("Number of duplicate rows:", df.duplicated().sum())
    print("\nBasic statistics:\n", df.describe())
    print("\nFirst few rows:\n", df.head())

df = consumption_data_loader("data/raw/data.csv")
