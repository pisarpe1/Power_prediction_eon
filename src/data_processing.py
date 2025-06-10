import pandas as pd

def check_duplicate_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes duplicate rows from the DataFrame and returns the cleaned DataFrame.
    By default, keeps the first occurrence of each duplicate row.
    """
    print(f"Number of duplicate rows: {df.duplicated().sum()}")
    df = df.drop_duplicates()
    return df

def check_non_numeric_values_in_values_column(df: pd.DataFrame) -> bool:
    """
    Checks if all values in the 'Values' column are numeric.
    Returns True if all values are numeric, otherwise False.
    """
    if 'Values' not in df.columns:
        raise KeyError("Column 'Values' not found in DataFrame.")
    non_numeric = pd.to_numeric(df['Values'], errors='coerce').isna()
    non_numeric = non_numeric & ~df['Values'].isna()
    return not non_numeric.any()
