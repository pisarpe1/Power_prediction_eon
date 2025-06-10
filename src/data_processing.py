import copy
import pandas as pd

from src.data_loader import RawConsumptionData


class ProcessedData:
    def __init__(self, raw_data: RawConsumptionData):
        self.raw_data = raw_data
        self.data = copy.deepcopy(raw_data.get_raw_data)

    @property
    def get_data(self) -> pd.DataFrame:
        return self.data

    def check_and_handle_duplicate_rows(self):
        """
        Identifies and removes duplicate rows from the DataFrame.
        """
        print(f"Number of duplicate rows: {self.data.duplicated().sum()}")
        self.data = self.data.drop_duplicates()

    def check_and_handle_missing_values(self) -> None:
        """
        Checks for missing values in the dataset, prints the count of missing values per column,
        and removes any rows containing missing values from the data.
        """
        
        missing_values = self.get_data.isnull().sum()
        self.data = self.data.dropna()
        print("Missing values per column:\n", missing_values)

    def check_and_handle_non_numeric_values_in_values_column(self) -> bool:
        """
        Attempts to convert all values in the 'Values' column to numeric.
        Non-convertible values are removed from the DataFrame.
        Returns True if all values are numeric after processing, otherwise False.
        """
        if 'Values' not in self.data.columns:
            raise KeyError("Column 'Values' not found in DataFrame.")
        # Attempt conversion; non-convertible values become NaN
        self.data['Values'] = pd.to_numeric(self.data['Values'], errors='coerce')
        # Count non-numeric (now NaN) values
        non_numeric_count = self.data['Values'].isna().sum()
        if non_numeric_count > 0:
            print(f"Removing {non_numeric_count} non-numeric values from 'Values' column.")
            self.data = self.data.dropna(subset=['Values'])
        # After cleaning, check if any non-numeric values remain
        return self.data['Values'].notna().all()


    def run_data_checks(self) -> None:
        """
        Runs a series of data checks on the DataFrame.
        Prints the results of each check.
        """
        print("\n--- Data Checks ---")
        
        # Check for duplicate rows
        self.check_and_handle_duplicate_rows()

        # Check for missing values
        self.check_and_handle_missing_values()

        # Check for non-numeric values in 'Values' column
        if not self.check_and_handle_non_numeric_values_in_values_column():
            print("Warning: Non-numeric values found in 'Values' column.")

        # Print first few rows
        print("\nFirst few rows:\n", self.data.head())

