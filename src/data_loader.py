import pandas as pd


class RawConsumptionData:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.raw_data = self._consumption_data_loader()

    def _consumption_data_loader(self) -> pd.DataFrame:
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
            load_data = pd.read_csv(self.file_path, sep=';', parse_dates=['Date'], dayfirst=True)
            load_data.set_index('Date', inplace=True)
            print(f"Data successfully loaded from {self.file_path}.")

        except FileNotFoundError:
            print(f"File {self.file_path} not found.")
            exit(1)
        except ValueError as e:
            if "Missing column provided to 'parse_dates': 'Date'" in str(e):
                print("Column 'Date' not found in the file.")
                exit(1)
            else:
                raise

        return load_data
    
    @property
    def get_raw_data(self) -> pd.DataFrame:
        return self.raw_data


