from meteostat import Point, Hourly
from datetime import datetime
import pandas as pd
import holidays
import numpy as np

PLACES = {  # Dictionary of cities with their geographical coordinates for data collection
    'Praha': Point(50.0755, 14.4378),
    'Brno': Point(49.1951, 16.6068),
    'Ostrava': Point(49.8209, 18.2625),
    'Plzen': Point(49.7475, 13.3776),
    'Liberec': Point(50.7671, 15.0562),
    'Ceske_Budejovice': Point(48.9745, 14.4743)
    }

TIMESTART = datetime(2023, 1, 1, 0) # Start time for data collection
TIMEEND = datetime(2024, 4, 22, 8)  # End time for data collection

class TemperatureData:
    """
    TemperatureData class is responsible for collecting, processing, and storing temperature data 
    for specified locations and time periods. It also provides a preview of the processed data.
    Attributes:
        _places (dict): A dictionary containing city names as keys and their geographical coordinates as values.
        _timestart (str): The start time for fetching temperature data.
        _timeend (str): The end time for fetching temperature data.
        temperature_cz (pd.DataFrame): A DataFrame containing temperature data for the specified locations 
                                       and the average temperature across all locations.
    Methods:
        __init__():
            Initializes the TemperatureData object, collects temperature data, stores it in a CSV file, 
            and displays a preview of the data.
        colect_temperature_data():
            Collects hourly temperature data for the specified locations and time period, calculates the 
            average temperature across all locations, and stores the data in a DataFrame.
        store_temperature_in_csv():
            Saves the average temperature data to a CSV file named 'prumerna_teplota_CR.csv' in the 'data' directory.
        temperature_data_view():
            Prints a preview of the average temperature data.
    """
    def __init__(self):
        self._places = PLACES
        self._timestart = TIMESTART
        self._timeend = TIMEEND
        self.unit = '°C'  # Temperature unit
        self.temperature_cz = self.colect_temperature_data()
        self.store_temperature_in_csv()
        self.temperature_data_view()

    def colect_temperature_data(self):
        data_teploty = pd.DataFrame()

        for city, geo in self._places.items():
            data = Hourly(geo, self._timestart, self._timeend).fetch()
            data_teploty[city] = data['temp']   # ['°C']

        data_teploty['Prumer_CR_teploty'] = data_teploty.mean(axis=1)

        self.temperature_cz = data_teploty
        
        return data_teploty
    

    def store_temperature_in_csv(self):

        self.temperature_cz[['Prumer_CR_teploty']].to_csv('data/prumerna_teplota_CR.csv', sep=';')

    def temperature_data_view(self) -> None:
        print("\nTemperature data:\n", self.temperature_cz[['Prumer_CR_teploty']].head())

class SunshineData:
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
        self._places = PLACES
        self._timestart = TIMESTART
        self._timeend = TIMEEND
        self.unit = 'min/h'
        self.sunshine_cz = self.collect_sunshine_data()
        self.store_sunshine_in_csv()
        self.sunshine_data_view()

    def collect_sunshine_data(self):
        sunshine_df = pd.DataFrame()

        for city, geo in self._places.items():
            data = Hourly(geo, self._timestart, self._timeend).fetch()
            sunshine_df[city] = data['tsun']

        sunshine_df['Prumer_CR_svit'] = sunshine_df.mean(axis=1)
        self.sunshine_cz = sunshine_df

        return sunshine_df

    def store_sunshine_in_csv(self):
        self.sunshine_cz[['Prumer_CR_svit']].to_csv('data/prumerny_osvit_CR.csv', sep=';')

    def sunshine_data_view(self):
        print("\nSunshine data:\n", self.sunshine_cz[['Prumer_CR_svit']].head())

class WindData:
    """
    A class to collect, process, and store wind speed data for specified locations and time periods.
    Attributes:
        _places (dict): A dictionary containing city names as keys and their geographical coordinates as values.
        _timestart (str): The start time for data collection in ISO 8601 format.
        _timeend (str): The end time for data collection in ISO 8601 format.
        wind_cz (pd.DataFrame): A DataFrame containing wind speed data for specified locations and their average.
    Methods:
        collect_wind_data():
            Collects wind speed data for specified locations and time periods, calculates the average wind speed
            across all locations, and stores the data in a DataFrame.
        store_wind_in_csv():
            Saves the average wind speed data to a CSV file named 'prumerna_rychlost_vetru_CR.csv' in the 'data' directory.
        wind_data_view():
            Prints the first few rows of the average wind speed data for visualization.
    """
    def __init__(self):
        self._places = PLACES
        self._timestart = TIMESTART
        self._timeend = TIMEEND
        self.unit = 'km/h'  # Wind speed unit
        self.wind_cz = self.collect_wind_data()
        self.store_wind_in_csv()
        self.wind_data_view()

    def collect_wind_data(self):
        wind_df = pd.DataFrame()

        for city, geo in self._places.items():
            data = Hourly(geo, self._timestart, self._timeend).fetch()
            wind_df[city] = data['wspd']

        wind_df['Prumer_CR_vitr'] = wind_df.mean(axis=1)
        self.wind_cz = wind_df

        return wind_df

    def store_wind_in_csv(self):
        self.wind_cz[['Prumer_CR_vitr']].to_csv('data/prumerna_rychlost_vetru_CR.csv', sep=';')

    def wind_data_view(self):
        print("\nWind data:\n", self.wind_cz[['Prumer_CR_vitr']].head())

class CalendarData:
    """
    CalendarData class generates and stores calendar information for a specified time range.
    Attributes:
        _timestart (datetime): The start time for the calendar data.
        _timeend (datetime): The end time for the calendar data.
        cz_holidays (holidays.HolidayBase): A list of Czech holidays within the specified time range.
        calendar_cz (pd.DataFrame): A DataFrame containing calendar information such as day of the week, weekend status, and holiday status.
    Methods:
        __init__():
            Initializes the CalendarData object, generates calendar information, stores it as a CSV file, and prints a preview.
        _generate_calendar_info() -> pd.DataFrame:
            Generates a DataFrame with calendar information including day of the week, weekend status, and holiday status.
        _store_calendar_csv():
            Saves the generated calendar information to a CSV file.
        calendar_preview():
            Prints a preview of the generated calendar information.
    """
    def __init__(self):
        self._timestart = TIMESTART
        self._timeend = TIMEEND
        self.cz_holidays = holidays.CZ(years=range(self._timestart.year, self._timeend.year + 1))
        self.calendar_cz = self._generate_calendar_info()
        self._store_calendar_csv()
        self.calendar_preview()

    def _generate_calendar_info(self) -> pd.DataFrame:
        # Create a time index with hourly steps
        time_index = pd.date_range(start=self._timestart, end=self._timeend, freq='h')

        # Create a DataFrame with calendar information
        df = pd.DataFrame(index=time_index)
        df['day_of_week'] = df.index.dayofweek
        df['is_weekend'] = df['day_of_week'] >= 5
        df['is_holiday'] = np.isin(df.index.date, list(self.cz_holidays))
        return df

    def _store_calendar_csv(self):
        self.calendar_cz.to_csv('data/calendar_info.csv', sep=';')

    def calendar_preview(self):
        print("\nCalendar data:\n", self.calendar_cz.head())


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
