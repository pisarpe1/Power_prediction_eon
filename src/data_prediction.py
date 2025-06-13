import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from xgboost import XGBRegressor
import joblib

class EnergyPredictor:
    def __init__(self, db_path, table_name='energy_data'):
        self.db_path = db_path
        self.table_name = table_name
        self.df = None
        self.model = XGBRegressor()
        self.X_train = self.X_test = self.y_train = self.y_test = None
        self.load_data()
        self.preprocess()
        self.split_data()
        self.train()
        self.save_model()

    def load_data(self):
        conn = sqlite3.connect(self.db_path)
        self.df = pd.read_sql_query(f"SELECT * FROM {self.table_name}", conn)
        conn.close()
        print("Data načtena")

    def preprocess(self):
        df = self.df.copy()
        # Vytvoření timestampu
        df['timestamp'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
        df = df.sort_values('timestamp')
        # Odstranění nepoužitelných sloupců
        X = df.drop(columns=['consumption', 'timestamp'])
        y = df['consumption']
        # Odstranění nečíselných sloupců
        X = X.select_dtypes(include=['number', 'bool', 'category'])
        self.X = X
        self.y = y
        print("Data předzpracována")

    def split_data(self, test_size=0.2):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=test_size, shuffle=False
        )
        print("Data rozdělena na trénovací a testovací sady")

    def train(self):
        self.model.fit(self.X_train, self.y_train)
        print("Model natrénován")

    def evaluate(self):
        y_pred = self.model.predict(self.X_test)
        mae = mean_absolute_error(self.y_test, y_pred)
        print(f" MAE (Mean Absolute Error): {mae:.2f}")
        return mae

    def predict(self, new_data):
        """
        new_data: DataFrame se stejnou strukturou jako X (bez 'consumption' a 'timestamp')
        """
        predictions = self.model.predict(new_data)
        return predictions
    
    def save_model(self, filename='outputs/energy_model.pkl'):
        joblib.dump(self.model, filename)
        print(f"Model uložen do souboru: {filename}")

    def load_model(self, filename='outputs/energy_model.pkl'):
        self.model = joblib.load(filename)
        print(f"Model načten ze souboru: {filename}")

    def show_model_info(self):
        print("Model Info:")
        print(f"  - Model type: {type(self.model).__name__}")
        print(f"  - Number of features: {self.X_train.shape[1]}")
        print(f"  - Training samples: {self.X_train.shape[0]}")
        print(f"  - Test samples: {self.X_test.shape[0]}")
        print(f"  - Features: {list(self.X_train.columns)}")
