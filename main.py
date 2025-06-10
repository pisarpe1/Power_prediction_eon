from src.data_loader import RawConsumptionData
from src.data_processing import ProcessedData


raw_data = RawConsumptionData('data/raw/data.csv')

processing_data = ProcessedData(raw_data)

processing_data.run_data_checks()

