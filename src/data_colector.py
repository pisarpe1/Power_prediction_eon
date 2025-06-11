import os
from meteostat import Point, Hourly
from datetime import datetime
import pandas as pd
import holidays
import numpy as np

PLACES = {  # Dictionary of cities with their geographical coordinates for data collection
    'Praha': Point(50.0755, 14.4378),
    'Plzen': Point(49.7475, 13.3776),
    'Liberec': Point(50.7671, 15.0562),
    'Ceske_Budejovice': Point(48.9745, 14.4743)
    }

TIMESTART = datetime(2023, 1, 1, 0) # Start time for data collection
TIMEEND = datetime(2024, 4, 22, 8)  # End time for data collection

class DataCollector:
    """
    A parent class for collecting, processing, and storing various types of data.
    Attributes:
        _places (dict): A dictionary containing city names as keys and their geographical coordinates as values.
        _timestart (datetime): The start time for data collection.
        _timeend (datetime): The end time for data collection.
        storage_path (str): The file path where the collected data will be stored.
    Methods:
        collect_data():
            Abstract method to be implemented by child classes for collecting specific types of data.
        store_data_in_csv():
            Saves the collected data to a CSV file.
        data_preview():
            Prints a preview of the collected data.
    """
    def __init__(self, file_name):
        self._places = PLACES
        self._timestart = TIMESTART
        self._timeend = TIMEEND
        self.storage_path = 'data/external/'
        self.file_name = file_name
        self._ensure_directory_exists()

    def collect_data(self):
        raise NotImplementedError("Subclasses must implement the collect_data method.")

    def store_data_in_csv(self):

        # Save the data to CSV
        if self.data is not None:
            self.data.to_csv(os.path.join(self.storage_path, self.file_name), sep=';')
        else:
            print("No data to store.")

    def _ensure_directory_exists(self):
        """
        Ensures the directory for the given path exists. If not, creates it.
        """
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)

    def data_preview(self, file_name=None):
        if self.data is not None:
            print(f"\nData preview {file_name}:\n {self.data.head()}")
        else:
            print(f"No data {file_name} to preview.")


class TemperatureData(DataCollector):
    """
    TemperatureData class is responsible for collecting, processing, and storing temperature data 
    for specified locations and time periods. It also provides a preview of the processed data.
    Attributes:
        _places (dict): A dictionary containing city names as keys and their geographical coordinates as values.
        _timestart (datetime): The start time for fetching temperature data.
        _timeend (datetime): The end time for fetching temperature data.
        temperature_cz (pd.DataFrame): A DataFrame containing temperature data for the specified locations 
                                       and the average temperature across all locations.
    Methods:
        __init__():
            Initializes the TemperatureData object, collects temperature data, stores it in a CSV file, 
            and displays a preview of the data.
        collect_temperature_data():
            Collects hourly temperature data for the specified locations and time period, calculates the 
            average temperature across all locations, and stores the data in a DataFrame.
        store_temperature_in_csv():
            Saves the average temperature data to a CSV file named 'temperature_data.csv' in the 'data/external' directory.
        temperature_data_view():
            Prints a preview of the average temperature data.
    """
    def __init__(self):
        self.file_name = 'temperature_data.csv'
        super().__init__(self.file_name)
        self.unit = '°C'  # Temperature unit
        self.data = self.collect_data()
        self.store_data_in_csv()
        self.data_preview(self.file_name)

    def collect_data(self):
        temperature_df = pd.DataFrame()

        for city, geo in self._places.items():
            data = Hourly(geo, self._timestart, self._timeend).fetch()
            temperature_df[city] = data['temp']

        temperature_df['average'] = temperature_df.mean(axis=1)

        return temperature_df


class SunshineData(DataCollector):
    """
    A class to collect, process, and store sunshine data for specified locations.
    Attributes:
        _places (dict): A dictionary containing city names as keys and their geographical coordinates as values.
        _timestart (str): The start time for data collection in a specific format.
        _timeend (str): The end time for data collection in a specific format.
        sunshine_cz (pd.DataFrame): A DataFrame containing sunshine data for all locations and their average.
    Methods:
        __init__():
            Initializes the SunshineData object, collects sunshine data, stores it in a CSV file, 
            and displays a preview of the data.
        collect_sunshine_data():
            Collects sunshine data for all specified locations within the given time range.
            Returns:
                pd.DataFrame: A DataFrame containing sunshine data for each location and their average.
        store_sunshine_in_csv():
            Stores the average sunshine data for the Czech Republic in a CSV file.
        sunshine_data_view():
            Displays a preview of the average sunshine data for the Czech Republic.
    """

    def __init__(self):
        self.file_name ='solar_data.csv'
        super().__init__(self.file_name)
        self.unit = 'min/h'
        self.data = self.collect_data()
        self.store_data_in_csv()
        self.data_preview(self.file_name)

    def collect_data(self):
        sunshine_df = pd.DataFrame()

        for city, geo in self._places.items():
            data = Hourly(geo, self._timestart, self._timeend).fetch()
            sunshine_df[city] = data['tsun']

        sunshine_df['average'] = sunshine_df.mean(axis=1)

        return sunshine_df


class WindData(DataCollector):
    """
    A class to collect, process, and store wind speed data for specified locations and time periods.
    Attributes:
        _places (dict): A dictionary containing city names as keys and their geographical coordinates as values.
        _timestart (datetime): The start time for data collection.
        _timeend (datetime): The end time for data collection.
        data (pd.DataFrame): A DataFrame containing wind speed data for specified locations and their average.
    Methods:
        __init__():
            Initializes the WindData object, collects wind speed data, stores it in a CSV file, 
            and displays a preview of the data.
        collect_data():
            Collects wind speed data for specified locations and time periods, calculates the average wind speed
            across all locations, and stores the data in a DataFrame.
        store_data_in_csv():
            Saves the average wind speed data to a CSV file.
        data_preview():
            Prints the first few rows of the average wind speed data for visualization.
    """
    def __init__(self):
        self.file_name = 'wind_data.csv'
        super().__init__(self.file_name)
        self.unit = 'km/h'  # Wind speed unit
        self.data = self.collect_data()
        self.store_data_in_csv()
        self.data_preview(self.file_name)

    def collect_data(self):
        wind_df = pd.DataFrame()

        for city, geo in self._places.items():
            data = Hourly(geo, self._timestart, self._timeend).fetch()
            wind_df[city] = data['wspd']

        wind_df['average'] = wind_df.mean(axis=1)

        return wind_df


class CalendarData(DataCollector):
    """
    CalendarData class generates and stores calendar information for a specified time range.
    Attributes:
        _places (dict): Not used in this class, but inherited from DataCollector.
        _timestart (datetime): The start time for the calendar data.
        _timeend (datetime): The end time for the calendar data.
        cz_holidays (holidays.HolidayBase): A list of Czech holidays within the specified time range.
        data (pd.DataFrame): A DataFrame containing calendar information such as day of the week, weekend status, and holiday status.
    Methods:
        __init__():
            Initializes the CalendarData object, generates calendar information, stores it as a CSV file, and prints a preview.
        collect_data() -> pd.DataFrame:
            Generates a DataFrame with calendar information including day of the week, weekend status, and holiday status.
        store_data_in_csv():
            Saves the generated calendar information to a CSV file.
        data_preview():
            Prints a preview of the generated calendar information.
    """
    def __init__(self):
        self.file_name = 'calendar_data.csv'
        super().__init__(self.file_name)
        self.cz_holidays = holidays.CZ(years=range(self._timestart.year, self._timeend.year + 1))
        self.data = self.collect_data()
        self.store_data_in_csv()
        self.data_preview(self.file_name)

    def collect_data(self) -> pd.DataFrame:
        # Create a time index with hourly steps
        time_index = pd.date_range(start=self._timestart, end=self._timeend, freq='h')

        # Create a DataFrame with calendar information
        df = pd.DataFrame(index=time_index)
        df['day_of_week'] = df.index.dayofweek
        df['is_weekend'] = df['day_of_week'] >= 5
        df['is_holiday'] = np.isin(df.index.date, list(self.cz_holidays))

        # Reset index and rename columns for desired output format
        df = df.reset_index()
        df.rename(columns={'index': 'time'}, inplace=True)

        # Set "time" as the index and remove the first column
        df.set_index('time', inplace=True)

        return df


"""
TODO: Implementace sběru dat o spotové ceně elektřiny z ENTSO-E pomocí API.
from entsoe import EntsoePandasClient
class PriceData:
    # nutná registrace a generování API key v https://transparency.entsoe.eu/
    def __init__(self):
        self.client = EntsoePandasClient(api_key='TVŮJ_API_KLÍČ')       # Nastav svůj API klíč
        self.country = 'CZ'
        self.timestart = pd.Timestamp('20230101', tz='Europe/Prague')
        self.timeend = pd.Timestamp('20240422 08:00', tz='Europe/Prague')
        self.prices_data = self.get_prices()


    def get_prices(self):
        # Získání cen (v EUR/MWh)
        prices = client.query_day_ahead_prices(self.country, start=self.timestart, end=self.timeend)
        return prices

    def store_prices_in_csv(self):

    # Uložení do CSV
    prices.to_csv('data/spotova_cena_elektřiny_CZ.csv')

    # Náhled
    print(prices.head())"""
