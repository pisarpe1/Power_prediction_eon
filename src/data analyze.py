import pandas as pd


def merged_data_loader(path: str) -> pd.DataFrame:
        try:
            load_data = pd.read_csv(path, sep=';', parse_dates=['datetime'], dayfirst=True)
            load_data.set_index('datetime', inplace=True)
            print(f"Data from {path} successfully loaded.")
        except FileNotFoundError:
            print(f"File {path} not found.")
            exit(1)
        except ValueError as e:
            if "Missing column provided to 'parse_dates': 'datetime'" in str(e):
                print(f"Column 'datetime' not found in the file {path}.")
                exit(1)
            else:
                exit(1)
        return load_data