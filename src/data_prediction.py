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
        print("Data loaded")

    def preprocess(self):
        df = self.df.copy()

        df['timestamp'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
        df = df.sort_values('timestamp')

        X = df.drop(columns=['consumption', 'timestamp'])
        y = df['consumption']

        X = X.select_dtypes(include=['number', 'bool', 'category'])
        self.X = X
        self.y = y
        print("Data preprocessed")

    def split_data(self, test_size=0.2):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=test_size, shuffle=False
        )
        print("Data split into training and test sets")

    def train(self):
        self.model.fit(self.X_train, self.y_train)
        print("Model trained")

    def evaluate(self):
        y_pred = self.model.predict(self.X_test)
        mae = mean_absolute_error(self.y_test, y_pred)
        print(f" MAE (Mean Absolute Error): {mae:.2f}")
        return mae

    def predict(self, new_data):
        """
        new_data: DataFrame with the same structure as X (without 'consumption' and 'timestamp')
        """
        predictions = self.model.predict(new_data)
        return predictions
    
    def save_model(self, filename='outputs/energy_model.pkl'):
        joblib.dump(self.model, filename)
        print(f"Model saved to file: {filename}")

    def load_model(self, filename='outputs/energy_model.pkl'):
        self.model = joblib.load(filename)
        print(f"Model loaded from file: {filename}")

    def show_model_info(self):
        print("Model Info:")
        print(f"  - Model type: {type(self.model).__name__}")
        print(f"  - Number of features: {self.X_train.shape[1]}")
        print(f"  - Training samples: {self.X_train.shape[0]}")
        print(f"  - Test samples: {self.X_test.shape[0]}")
        print(f"  - Features: {list(self.X_train.columns)}")

def load_last_week_data_from_db(db_path, table_name='energy_data'):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    conn.close()
    df['timestamp'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
    df = df.sort_values('timestamp')
    last_week = df.tail(7 * 24)  # last 7 days by hour
    return last_week

def predict_last_week(predictor, last_week):
    X = last_week.drop(columns=['consumption'], errors='ignore')
    X = X.select_dtypes(include=['number', 'bool', 'category'])
    predictions = predictor.predict(X)
    last_week = last_week.copy()
    last_week['predicted_consumption'] = predictions
    return last_week

def save_predictions_to_csv(df, filename='outputs/predictions_last_week.csv'):
    df.to_csv(filename, index=False)
    print(f"Predictions saved to {filename}")

import matplotlib.pyplot as plt

def compare_real_vs_predicted(df):
    mae = ((df['consumption'] - df['predicted_consumption']).abs()).mean()
    print(f"MAE last week: {mae:.2f}")
    plt.figure(figsize=(14, 6))
    plt.plot(df['timestamp'], df['consumption'], label='Actual consumption')
    plt.plot(df['timestamp'], df['predicted_consumption'], label='Predicted consumption')
    plt.xlabel('Time')
    plt.ylabel('Consumption')
    plt.title('Comparison of actual and predicted consumption (last week)')
    plt.legend()
    plt.tight_layout()
    plt.savefig('outputs/real_vs_predicted_last_week.png')
    #plt.show()

def predicted_last_week_data():
    print("Creating prediction model data...")
    predictor = EnergyPredictor(db_path="data/database.db")
    last_week = load_last_week_data_from_db('data/database.db')
    result = predict_last_week(predictor, last_week)
    save_predictions_to_csv(result)
    compare_real_vs_predicted(result)
