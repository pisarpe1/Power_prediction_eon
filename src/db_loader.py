from datetime import datetime
import csv
import sqlite3

class EnergyDataDB:
    def __init__(self, db_path="data/database.db", csv_path="data/processed/merged_data.csv"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.c = self.conn.cursor()
        self.create_table()
        self.load_csv(csv_path)

    def create_table(self):
        self.c.execute("""
        CREATE TABLE IF NOT EXISTS energy_data (
            datetime TEXT PRIMARY KEY,
            year INTEGER,
            month INTEGER,
            day INTEGER,
            hour INTEGER,
            consumption REAL,
            temperature_average REAL,
            solar_average REAL,
            wind_average REAL,
            day_of_week INTEGER,
            is_weekend BOOLEAN,
            is_holiday BOOLEAN
        )
        """)
        self.conn.commit()

    def load_csv(self, csv_path):
        with open(csv_path, newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=';')
            rows = []
            for row in reader:
                dt = datetime.strptime(row["datetime"], "%Y-%m-%d %H:%M:%S")
                rows.append((
                    row["datetime"],
                    dt.year,
                    dt.month,
                    dt.day,
                    dt.hour,
                    float(row["consumption"]),
                    float(row["temperature_average"]),
                    float(row["solar_average"]),
                    float(row["wind_average"]),
                    int(row["day_of_week"]),
                    row["is_weekend"] == "True",
                    row["is_holiday"] == "True"
                ))
        self.c.executemany("""
        INSERT OR REPLACE INTO energy_data
        (datetime, year, month, day, hour, consumption, temperature_average, solar_average, wind_average, day_of_week, is_weekend, is_holiday)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, rows)
        self.conn.commit()

    def close(self):
        self.conn.close()

    def db_query(self, query, params=None):
        """
        Execute a SQL query on the energy_data table.
        Args:
            query (str): The SQL query to execute.
            params (tuple, optional): Parameters to use with the query.
        Returns:
            list: Query results as a list of tuples.
        """
        if params is None:
            params = ()
        self.c.execute(query, params)
        return self.c.fetchall()

    def get_consumption_per_year(self):
        """
        Returns total consumption per year as a list of (year, total_consumption) tuples.
        """
        self.c.execute("""
            SELECT year, SUM(consumption) as total_consumption
            FROM energy_data
            GROUP BY year
            ORDER BY year
        """)
        return self.c.fetchall()

    def get_average_consumption_per_year(self):
        """
        Returns average consumption per year as a list of (year, avg_consumption) tuples.
        """
        self.c.execute("""
            SELECT year, AVG(consumption) as avg_consumption
            FROM energy_data
            GROUP BY year
            ORDER BY year
        """)
        return self.c.fetchall()
