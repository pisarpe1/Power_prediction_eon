import copy
import pandas as pd

from src.data_loader import RawData


class ProcessedData:
    def __init__(self, raw_data: RawData):
        self.raw_data = raw_data.get_raw_data() # Store the raw data from RawData instance
        self.data = self.pick_raw_data()
        self.rename_average_columns()
        self.run_data_checkers()
        self.merged_data = self.merge_raw_data()
        self.save_merged_data('data/processed/merged_data.csv')

    def pick_raw_data(self) -> dict:
        data = copy.deepcopy(self.raw_data)
        data = {
            'consumption': data['consumption'],
            'temperature': data['temperature'][['average']],
            'calendar': data['calendar'],
            'solar': data['solar'][['average']],
            'wind': data['wind'][['average']]
        }
        
        return data
    
    def rename_average_columns(self) -> None:
        """
        Renames the 'average' columns in the data to more descriptive names.
        """
        self.data['consumption'].rename(columns={'Values': 'consumption'}, inplace=True)
        self.data['temperature'].rename(columns={'average': 'temperature_average'}, inplace=True)
        self.data['solar'].rename(columns={'average': 'solar_average'}, inplace=True)
        self.data['wind'].rename(columns={'average': 'wind_average'}, inplace=True)
        print("Average columns renamed successfully.")

    def save_merged_data(self, path: str) -> None:
        """
        Saves the merged raw data to a CSV file.
        Args:
            path (str): The file path where the merged data will be saved.
        """
        self.merged_data.to_csv(path, sep=';')
        print(f"Merged data saved to {path}.")
    
    def merge_raw_data(self) -> pd.DataFrame:

        # Ensure indices are of the same type before merging
        self.data['consumption'].index = pd.to_datetime(self.data['consumption'].index)
        self.data['temperature'].index = pd.to_datetime(self.data['temperature'].index)
        self.data['solar'].index = pd.to_datetime(self.data['solar'].index)
        self.data['wind'].index = pd.to_datetime(self.data['wind'].index)
        self.data['calendar'].index = pd.to_datetime(self.data['calendar'].index)   
        
        # Merge data based on index
        merged_data = self.data['consumption'].merge(self.data['temperature'], left_index=True, right_index=True, how="left")
        merged_data = merged_data.merge(self.data['solar'], left_index=True, right_index=True, how="left")
        merged_data = merged_data.merge(self.data['wind'], left_index=True, right_index=True, how="left")
        merged_data = merged_data.merge(self.data['calendar'], left_index=True, right_index=True, how="left")

      
        return merged_data
        
    def check_time_line(self) -> pd.DataFrame:
        # Check if indices are unique for each dataset and update self.data
        for key in self.data.keys():
            if not self.data[key].index.is_unique:
                print(f"Warning: Duplicate indices in {key.capitalize()}:", self.data[key].index[self.data[key].index.duplicated()])
                self.data[key] = self.data[key][~self.data[key].index.duplicated()]
    
    def check_missing_values(self) -> pd.DataFrame:
        """
        Checks for missing data in the datasets and prints warnings if missing values are found.
        Returns:
            DataFrame: A DataFrame containing the count of missing values for each column.
        """
        missing_data = {key: df.isnull().sum() for key, df in self.data.items()}
        
        for key, missing in missing_data.items():
            if missing.sum() > 0:
                print(f"Warning: Missing values detected in {key.capitalize()} dataset:")
                print(missing[missing > 0])
        
        return pd.DataFrame(missing_data)

    def check_data_type(self) -> None:
        """
        Checks if all values in each column of the datasets have the same type.
        Prints warnings if inconsistent types are found.
        """
        for key, df in self.data.items():
            for column in df.columns:
                unique_types = df[column].map(type).unique()
                if len(unique_types) > 1:
                    print(f"Warning: Column '{column}' in {key.capitalize()} dataset has inconsistent types: {unique_types}")
                else:
                    pass
                    #print(f"Column '{column}' in {key.capitalize()} dataset has consistent type: {unique_types[0]}")

    def run_data_checkers(self):
        """
        Runs data checkers to ensure the integrity of the data.
        """
        self.check_time_line()
        self.check_missing_values()
        self.check_data_type()
        print("Data checkers completed successfully.")
        

    