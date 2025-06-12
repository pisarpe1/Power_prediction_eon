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

    # Time interval total consumption methods
    def get_consumption_per_year(self, year=None):
        """
        Returns total consumption per year as a list of (year, total_consumption) tuples.
        If 'year' is specified, returns total consumption only for that year.
        """
        if year is not None:
            self.c.execute("""
                SELECT year, SUM(consumption) as total_consumption
                FROM energy_data
                WHERE year = ?
                GROUP BY year
                ORDER BY year
            """, (year,))
        else:
            self.c.execute("""
                SELECT year, SUM(consumption) as total_consumption
                FROM energy_data
                GROUP BY year
                ORDER BY year
            """)
        return self.c.fetchall()
    
    def get_consumption_per_month(self, year=None, month=None):
        """
        Returns total consumption per month as a list of (year, month, total_consumption) tuples.
        If 'year' and 'month' are specified, returns total consumption only for that month.
        If only 'year' is specified, returns total consumption for each month in that year.
        """
        if year is not None and month is not None:
            self.c.execute("""
                SELECT year, month, SUM(consumption) as total_consumption
                FROM energy_data
                WHERE year = ? AND month = ?
                GROUP BY year, month
                ORDER BY year, month
            """, (year, month))
        elif year is not None:
            self.c.execute("""
                SELECT year, month, SUM(consumption) as total_consumption
                FROM energy_data
                WHERE year = ?
                GROUP BY year, month
                ORDER BY year, month
            """, (year,))
        else:
            self.c.execute("""
                SELECT year, month, SUM(consumption) as total_consumption
                FROM energy_data
                GROUP BY year, month
                ORDER BY year, month
            """)
        return self.c.fetchall()
    
    def get_consumption_per_day(self, year=None, month=None, day=None):
        """
        Returns total consumption per day as a list of (year, month, day, total_consumption) tuples.
        If 'year', 'month', and 'day' are specified, returns total consumption only for that day.
        If 'year' and 'month' are specified, returns total consumption for each day in that month.
        If only 'year' is specified, returns total consumption for each day in that year.
        """
        if year is not None and month is not None and day is not None:
            self.c.execute("""
                SELECT year, month, day, SUM(consumption) as total_consumption
                FROM energy_data
                WHERE year = ? AND month = ? AND day = ?
                GROUP BY year, month, day
                ORDER BY year, month, day
            """, (year, month, day))
        elif year is not None and month is not None:
            self.c.execute("""
                SELECT year, month, day, SUM(consumption) as total_consumption
                FROM energy_data
                WHERE year = ? AND month = ?
                GROUP BY year, month, day
                ORDER BY year, month, day
            """, (year, month))
        elif year is not None:
            self.c.execute("""
                SELECT year, month, day, SUM(consumption) as total_consumption
                FROM energy_data
                WHERE year = ?
                GROUP BY year, month, day
                ORDER BY year, month, day
            """, (year,))
        else:
            self.c.execute("""
                SELECT year, month, day, SUM(consumption) as total_consumption
                FROM energy_data
                GROUP BY year, month, day
                ORDER BY year, month, day
            """)
        return self.c.fetchall()
    def get_consumption_per_hour(self, year=None, month=None, day=None):
        """
        Returns total consumption per hour as a list of (year, month, day, hour, total_consumption) tuples.
        If 'year', 'month', and 'day' are specified, returns total consumption only for that hour of that day.
        If 'year' and 'month' are specified, returns total consumption for each hour of that month.
        If only 'year' is specified, returns total consumption for each hour of that year.
        """
        if year is not None and month is not None and day is not None:
            self.c.execute("""
                SELECT year, month, day, hour, SUM(consumption) as total_consumption
                FROM energy_data
                WHERE year = ? AND month = ? AND day = ?
                GROUP BY year, month, day, hour
                ORDER BY year, month, day, hour
            """, (year, month, day))
        elif year is not None and month is not None:
            self.c.execute("""
                SELECT year, month, day, hour, SUM(consumption) as total_consumption
                FROM energy_data
                WHERE year = ? AND month = ?
                GROUP BY year, month, day, hour
                ORDER BY year, month, day, hour
            """, (year, month))
        elif year is not None:
            self.c.execute("""
                SELECT year, month, day, hour, SUM(consumption) as total_consumption
                FROM energy_data
                WHERE year = ?
                GROUP BY year, month, day, hour
                ORDER BY year, month, day, hour
            """, (year,))
        else:
            self.c.execute("""
                SELECT year, month, day, hour, SUM(consumption) as total_consumption
                FROM energy_data
                GROUP BY year, month, day, hour
                ORDER BY year, month, day, hour
            """)
        return self.c.fetchall()    

    # Time interval average consumption methods
    def get_average_consumption_per_year(self):
        """
        Returns average consumption per year as a list of (year, average_consumption) tuples.
        """
        self.c.execute("""
            SELECT year, AVG(consumption) as average_consumption
            FROM energy_data
            GROUP BY year
            ORDER BY year
        """)
        return self.c.fetchall()
    
    def get_average_consumption_per_month(self, year=None):
        """
        Returns average consumption per month as a list of (year, month, average_consumption) tuples.
        If 'year' is specified, returns average consumption for each month in that year.
        """
        if year is not None:
            self.c.execute("""
                SELECT year, month, AVG(consumption) as average_consumption
                FROM energy_data
                WHERE year = ?
                GROUP BY year, month
                ORDER BY year, month
            """, (year,))
        else:
            self.c.execute("""
                SELECT year, month, AVG(consumption) as average_consumption
                FROM energy_data
                GROUP BY year, month
                ORDER BY year, month
            """)
        return self.c.fetchall()
    
    def get_average_consumption_per_day(self, year=None, month=None):
        """
        Returns average consumption per day as a list of (year, month, day, average_consumption) tuples.
        If 'year' and 'month' are specified, returns average consumption for each day in that month.
        If only 'year' is specified, returns average consumption for each day in that year.
        """
        if year is not None and month is not None:
            self.c.execute("""
                SELECT year, month, day, AVG(consumption) as average_consumption
                FROM energy_data
                WHERE year = ? AND month = ?
                GROUP BY year, month, day
                ORDER BY year, month, day
            """, (year, month))
        elif year is not None:
            self.c.execute("""
                SELECT year, month, day, AVG(consumption) as average_consumption
                FROM energy_data
                WHERE year = ?
                GROUP BY year, month, day
                ORDER BY year, month, day
            """, (year,))
        else:
            self.c.execute("""
                SELECT year, month, day, AVG(consumption) as average_consumption
                FROM energy_data
                GROUP BY year, month, day
                ORDER BY year, month, day
            """)
        return self.c.fetchall()

    def get_average_consumption_per_hour(self, year=None, month=None, day=None):
        """
        Returns average consumption per hour as a list of (year, month, day, hour, average_consumption) tuples.
        If 'year', 'month', and 'day' are specified, returns average consumption for each hour of that day.
        If 'year' and 'month' are specified, returns average consumption for each hour of that month.
        If only 'year' is specified, returns average consumption for each hour of that year.
        """
        if year is not None and month is not None and day is not None:
            self.c.execute("""
                SELECT year, month, day, hour, AVG(consumption) as average_consumption
                FROM energy_data
                WHERE year = ? AND month = ? AND day = ?
                GROUP BY year, month, day, hour
                ORDER BY year, month, day, hour
            """, (year, month, day))
        elif year is not None and month is not None:
            self.c.execute("""
                SELECT year, month, day, hour, AVG(consumption) as average_consumption
                FROM energy_data
                WHERE year = ? AND month = ?
                GROUP BY year, month, day, hour
                ORDER BY year, month, day, hour
            """, (year, month))
        elif year is not None:
            self.c.execute("""
                SELECT year, month, day, hour, AVG(consumption) as average_consumption
                FROM energy_data
                WHERE year = ?
                GROUP BY year, month, day, hour
                ORDER BY year, month, day, hour
            """, (year,))
        else:
            self.c.execute("""
                SELECT year, month, day, hour, AVG(consumption) as average_consumption
                FROM energy_data
                GROUP BY year, month, day, hour
                ORDER BY year, month, day, hour
            """)
        return self.c.fetchall()
    
    def get_average_consumption_per_week(self):
        """
        Returns average consumption per week (Monday to Sunday) as a list of (week_start_date, average_consumption) tuples.
        week_start_date is the date (YYYY-MM-DD) of the Monday for each week.
        """
        self.c.execute("""
            SELECT 
                MIN(datetime) as week_start_date,
                AVG(consumption) as average_consumption
            FROM (
                SELECT 
                    *,
                    (strftime('%Y-%W', datetime) || '-1') as week_monday
                FROM energy_data
            )
            GROUP BY week_monday
            ORDER BY week_start_date
        """)
        # Convert week_start_date from 'YYYY-WW-1' to 'YYYY-MM-DD'
        results = []
        for week_start, avg in self.c.fetchall():
            # week_start is like '2023-05-1', convert to date
            try:
                year, week, _ = week_start.split('-')
                dt = datetime.strptime(f'{year}-{week}-1', '%Y-%W-%w')
                results.append((dt.strftime('%Y-%m-%d'), avg))
            except Exception:
                results.append((week_start, avg))
        return results
    


    # Time interval average consumption methods
    def get_average_consumption_per_year(self):
        """
        Returns average consumption and temperature per year as a list of (year, average_consumption, average_temperature) tuples.
        """
        self.c.execute("""
            SELECT year, AVG(consumption) as average_consumption, AVG(temperature_average) as average_temperature
            FROM energy_data
            GROUP BY year
            ORDER BY year
        """)
        return self.c.fetchall()

    def get_average_temperature_per_month(self, year=None):
        """
        Returns average consumption and temperature per month as a list of (year, month, average_consumption, average_temperature) tuples.
        If 'year' is specified, returns averages for each month in that year.
        """
        if year is not None:
            self.c.execute("""
                SELECT year, month, AVG(temperature_average) as average_temperature
                FROM energy_data
                WHERE year = ?
                GROUP BY year, month
                ORDER BY year, month
            """, (year,))
        else:
            self.c.execute("""
                SELECT year, month, AVG(temperature_average) as average_temperature
                FROM energy_data
                GROUP BY year, month
                ORDER BY year, month
            """)
        return self.c.fetchall()

    def get_average_temperature_per_day(self, year=None, month=None):
        """
        Returns average temperature per day as a list of (year, month, day, average_temperature) tuples.
        If 'year' and 'month' are specified, returns averages for each day in that month.
        If only 'year' is specified, returns averages for each day in that year.
        """
        if year is not None and month is not None:
            self.c.execute("""
                SELECT year, month, day, AVG(temperature_average) as average_temperature
                FROM energy_data
                WHERE year = ? AND month = ?
                GROUP BY year, month, day
                ORDER BY year, month, day
            """, (year, month))
        elif year is not None:
            self.c.execute("""
                SELECT year, month, day, AVG(temperature_average) as average_temperature
                FROM energy_data
                WHERE year = ?
                GROUP BY year, month, day
                ORDER BY year, month, day
            """, (year,))
        else:
            self.c.execute("""
                SELECT year, month, day, AVG(temperature_average) as average_temperature
                FROM energy_data
                GROUP BY year, month, day
                ORDER BY year, month, day
            """)
        return self.c.fetchall()
    def get_average_temperature_per_hour(self, year=None, month=None, day=None):
        """
        Returns average temperature per hour as a list of (year, month, day, hour, average_temperature) tuples.
        If 'year', 'month', and 'day' are specified, returns averages for each hour of that day.
        If 'year' and 'month' are specified, returns averages for each hour of that month.
        If only 'year' is specified, returns averages for each hour of that year.
        """
        if year is not None and month is not None and day is not None:
            self.c.execute("""
                SELECT year, month, day, hour, AVG(temperature_average) as average_temperature
                FROM energy_data
                WHERE year = ? AND month = ? AND day = ?
                GROUP BY year, month, day, hour
                ORDER BY year, month, day, hour
            """, (year, month, day))
        elif year is not None and month is not None:
            self.c.execute("""
                SELECT year, month, day, hour, AVG(temperature_average) as average_temperature
                FROM energy_data
                WHERE year = ? AND month = ?
                GROUP BY year, month, day, hour
                ORDER BY year, month, day, hour
            """, (year, month))
        elif year is not None:
            self.c.execute("""
                SELECT year, month, day, hour, AVG(temperature_average) as average_temperature
                FROM energy_data
                WHERE year = ?
                GROUP BY year, month, day, hour
                ORDER BY year, month, day, hour
            """, (year,))
        else:
            self.c.execute("""
                SELECT year, month, day, hour, AVG(temperature_average) as average_temperature
                FROM energy_data
                GROUP BY year, month, day, hour
                ORDER BY year, month, day, hour
            """)
        return self.c.fetchall()
    
    def get_average_solar_per_month(self, year=None):
        """
        Returns average solar radiation per month as a list of (year, month, average_solar) tuples.
        If 'year' is specified, returns averages for each month in that year.
        """
        if year is not None:
            self.c.execute("""
                SELECT year, month, AVG(solar_average) as average_solar
                FROM energy_data
                WHERE year = ?
                GROUP BY year, month
                ORDER BY year, month
            """, (year,))
        else:
            self.c.execute("""
                SELECT year, month, AVG(solar_average) as average_solar
                FROM energy_data
                GROUP BY year, month
                ORDER BY year, month
            """)
        return self.c.fetchall()
    

    