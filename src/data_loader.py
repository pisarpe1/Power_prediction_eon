import pandas as pd


class RawData:
    """
    RawData Class
    This class is responsible for loading and managing raw data from various sources, including consumption, temperature, calendar, solar, and wind data. It provides methods to load data from CSV files and retrieve the loaded data as pandas DataFrames.
    Attributes:
        raw_consumption_data (pd.DataFrame): DataFrame containing raw consumption data.
        raw_temperatur_data (pd.DataFrame): DataFrame containing raw temperature data.
        raw_calendar_data (pd.DataFrame): DataFrame containing raw calendar data.
        raw_solar_data (pd.DataFrame): DataFrame containing raw solar data.
        raw_wind_data (pd.DataFrame): DataFrame containing raw wind data.
    Methods:
        _consumption_data_loader(path: str) -> pd.DataFrame:
            Private method to load consumption data from a CSV file.
        _temperatur_data_loader(path: str) -> pd.DataFrame:
            Private method to load temperature data from a CSV file.
        _calendar_data_loader(path: str) -> pd.DataFrame:
            Private method to load calendar data from a CSV file.
        _solar_data_loader(path: str) -> pd.DataFrame:
            Private method to load solar data from a CSV file.
        _wind_data_loader(path: str) -> pd.DataFrame:
            Private method to load wind data from a CSV file.
        get_raw_consumption_data() -> pd.DataFrame:
            Public method to retrieve the raw consumption data.
        get_raw_temperatur_data() -> pd.DataFrame:
            Public method to retrieve the raw temperature data.
        get_raw_solar_data() -> pd.DataFrame:
            Public method to retrieve the raw solar data.
        get_raw_wind_data() -> pd.DataFrame:
            Public method to retrieve the raw wind data.
        get_raw_calendar_data() -> pd.DataFrame:
            Public method to retrieve the raw calendar data.
    """
    def __init__(self):
        self.raw_consumption_data = self._consumption_data_loader('data/raw/consumption_data.csv')
        self.raw_temperatur_data = self._temperatur_data_loader('data/external/temperature_data.csv')
        self.raw_calendar_data = self._calendar_data_loader('data/external/calendar_data.csv')
        self.raw_solar_data = self._solar_data_loader('data/external/solar_data.csv')
        self.raw_wind_data = self._wind_data_loader('data/external/wind_data.csv')


    def _consumption_data_loader(self, path: str) -> pd.DataFrame:
        try:
            load_data = pd.read_csv(path, sep=';', parse_dates=['Date'], dayfirst=True)
            load_data.set_index('Date', inplace=True)
            print(f"Data from {path} successfully loaded.")

        except FileNotFoundError:
            print(f"File {path} not found.")
            exit(1)
        except ValueError as e:
            if "Missing column provided to 'parse_dates': 'Date'" in str(e):
                print(f"Column 'Date' not found in the file {path} .")
                exit(1)
            else:
                raise

        return load_data
    
    def _temperatur_data_loader(self, path: str) -> pd.DataFrame:
        try:
            load_data = pd.read_csv(path, sep=';', parse_dates=['time'], dayfirst=True)
            load_data.set_index('time', inplace=True)
            print(f"Data from {path} successfully loaded.")

        except FileNotFoundError:
            print(f"File {path} not found.")
            exit(1)
        except ValueError as e:
            if "Missing column provided to 'parse_dates': 'time'" in str(e):
                print(f"Column 'time' not found in the file {path}.")
                exit(1)
            else:
                raise

        return load_data 
    
    def _calendar_data_loader(self, path: str) -> pd.DataFrame:
        try:
            load_data = pd.read_csv(path, sep=';', parse_dates=['time'], dayfirst=True)
            load_data.set_index('time', inplace=True)
            print(f"Data from {path} successfully loaded.")

        except FileNotFoundError:
            print(f"File {path} not found.")
            exit(1)
        except ValueError as e:
            if "Missing column provided to 'parse_dates': 'time'" in str(e):
                print(f"Column 'time' not found in the file{path} .")
                exit(1)
            else:
                raise

        return load_data   
    
    def _solar_data_loader(self, path: str) -> pd.DataFrame:
        try:
            load_data = pd.read_csv(path, sep=';', parse_dates=['time'], dayfirst=True)
            load_data.set_index('time', inplace=True)
            print(f"Data from {path} successfully loaded.")

        except FileNotFoundError:
            print(f"File {path} not found.")
            exit(1)
        except ValueError as e:
            if "Missing column provided to 'parse_dates': 'time'" in str(e):
                print(f"Column 'time' not found in the file{path} .")
                exit(1)
            else:
                raise

        return load_data
    
    def _wind_data_loader(self, path: str) -> pd.DataFrame:
        try:
            load_data = pd.read_csv(path, sep=';', parse_dates=['time'], dayfirst=True)
            load_data.set_index('time', inplace=True)
            print(f"Data from {path} successfully loaded.)")

        except FileNotFoundError:
            print(f"File {path} not found.")
            exit(1)
        except ValueError as e:
            if "Missing column provided to 'parse_dates': 'time'" in str(e):
                print(f"Column 'time' not found in the file.{path} ")
                exit(1)
            else:
                raise

        return load_data
    
    
    def get_raw_consumption_data(self) -> pd.DataFrame:
        return self.raw_consumption_data
    
    def get_raw_temperatur_data(self) -> pd.DataFrame:
        return self.raw_consumption_data
    
    def get_raw_solar_data(self) -> pd.DataFrame:
        return self.raw_solar_data    
   
    def get_raw_wind_data(self) -> pd.DataFrame:
        return self.raw_wind_data
    
    def get_raw_calendar_data(self) -> pd.DataFrame:
        return self.raw_calendar_data

