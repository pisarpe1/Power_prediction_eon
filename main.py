from src.data_colector import CalendarData, SunshineData, TemperatureData, WindData
from src.data_loader import RawData
from src.data_processing import ProcessedData


temperature_data = TemperatureData()
print(f"Temperature data length: {len(temperature_data.data)}")

sunshine_data = SunshineData()
print(f"Sunshine data length: {len(sunshine_data.data)}")
wind_data = WindData()
print(f"Wind data length: {len(wind_data.data)}")
calendar_data = CalendarData()
print(f"Calendar data length: {len(calendar_data.data)}")

raw_data = RawData()

"""processing_data = ProcessedData(raw_data)
print(f"Processed data length: {len(processing_data.get_data)}")"""


