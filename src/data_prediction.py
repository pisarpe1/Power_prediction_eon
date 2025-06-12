import sqlite3
import pandas as pd



class DataPredictor:
    def __init__(self, model, db_path='database.db', table_name='merged_data'):
        """
        model: A trained model object that implements a .predict() method (e.g., scikit-learn model).
        db_path: Path to the SQLite database file.
        table_name: Name of the table containing the data.
        """
        self.model = model
        self.db_path = db_path
        self.table_name = table_name
        self.data = self._load_data()

    def _load_data(self):
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query(f"SELECT * FROM {self.table_name}", conn)
        conn.close()
        return df

    def predict(self, input_data):
        """
        Makes a prediction using the trained model.
        input_data: DataFrame or array-like structure with features for prediction.
        """
        return self.model.predict(input_data)

    def predict_last_week_and_compare(self, datetime_col='datetime', target_col='consumption'):
        """
        Predicts consumption for the last week and compares with actual values.
        Returns a DataFrame with actual and predicted values.
        """
        df = self.data.copy()
        df[datetime_col] = pd.to_datetime(df[datetime_col])
        last_week = df[datetime_col].max() - pd.Timedelta(days=7)
        mask = df[datetime_col] > last_week
        last_week_data = df[mask]

        features = last_week_data.drop(columns=[target_col, datetime_col])
        actual = last_week_data[target_col].reset_index(drop=True)
        predicted = pd.Series(self.model.predict(features))

        comparison = pd.DataFrame({
            'datetime': last_week_data[datetime_col].reset_index(drop=True),
            'actual': actual,
            'predicted': predicted
        })
        return comparison
