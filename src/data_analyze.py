import os
import datetime
from collections import defaultdict
import numpy as np

import matplotlib.pyplot as plt

def show_month_data(database):
    """
    Plots total consumption and average temperature per month for all available years and saves the plot as a picture in the outputs folder.

    :param database: Database object with required query methods
    """

    results = database.get_consumption_per_month()
    results_temp = database.get_average_temperature_per_month()

    # Use datetime objects for direct timeline on x-axis
    months = [datetime.datetime(row[0], row[1], 1) for row in results]
    consumption = [row[2] for row in results]

    temp_months = [datetime.datetime(row[0], row[1], 1) for row in results_temp]
    avg_temp = [row[2] for row in results_temp]

    plt.figure(figsize=(14, 6))
    ax1 = plt.gca()

    # Plot total consumption
    line1, = ax1.plot(months, consumption, marker='o', label='Consumption [MWh]', color='tab:blue')
    ax1.set_xlabel('Date (Year-Month)')
    ax1.set_ylabel('Total Consumption [MWh]', color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    # Plot average temperature on secondary y-axis
    ax2 = ax1.twinx()
    line2, = ax2.plot(temp_months, avg_temp, marker='o', label='Temperature [°C]', color='tab:orange')
    ax2.set_ylabel('Temperature [°C]', color='tab:orange')
    ax2.tick_params(axis='y', labelcolor='tab:orange')

    # Format x-axis as year-month, auto-adjust for multiple years
    import matplotlib.dates as mdates
    ax1.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')

    # Combine legends
    lines = [line1, line2]
    labels = ['Consumption [MWh]', 'Temperature [°C]']
    ax1.legend(lines, labels)

    plt.title('Total Consumption per Month and Weather (All Years)')
    plt.tight_layout()

    # Save the plot to the outputs folder
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'outputs')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'consumption_temperature_monthly.png')
    plt.savefig(output_path)

    #plt.show()


def show_day_data(database):
    """
    Plots total consumption and average temperature per day for all available years, 
    and also shows the average per-day values for each day-of-year across all years.
    Saves the plot as a picture in the outputs folder.

    :param database: Database object with required query methods
    """

    results = database.get_consumption_per_day()
    results_temp = database.get_average_temperature_per_day()

    # Use datetime objects for direct timeline on x-axis
    days = [datetime.datetime(row[0], row[1], row[2]) for row in results]
    consumption = [row[3] for row in results]

    temp_days = [datetime.datetime(row[0], row[1], row[2]) for row in results_temp]
    avg_temp = [row[3] for row in results_temp]

    # Calculate average per day-of-year across all years

    doy_consumption = defaultdict(list)
    doy_temp = defaultdict(list)

    for dt, cons in zip(days, consumption):
        doy = dt.timetuple().tm_yday
        doy_consumption[doy].append(cons)

    for dt, temp in zip(temp_days, avg_temp):
        doy = dt.timetuple().tm_yday
        doy_temp[doy].append(temp)

    # Build average series for plotting
    avg_days = []
    avg_consumption = []
    avg_temperature = []

    # Use the first year in the data for x-axis reference
    if days:
        ref_year = min(dt.year for dt in days)
        for doy in sorted(doy_consumption.keys()):
            avg_days.append(datetime.datetime(ref_year, 1, 1) + datetime.timedelta(days=doy-1))
            avg_consumption.append(np.mean(doy_consumption[doy]))
            avg_temperature.append(np.mean(doy_temp[doy]))

    plt.figure(figsize=(16, 6))
    ax1 = plt.gca()

    # Plot total consumption
    line1, = ax1.plot(days, consumption, marker='.', linestyle='-', label='Consumption [MWh]', color='tab:blue')
    # Plot average consumption
    line1_avg, = ax1.plot(avg_days, avg_consumption, marker=None, linestyle='--', label='Avg Consumption [MWh] (all years)', color='tab:blue', alpha=0.5)
    ax1.set_xlabel('Date (Year-Month-Day)')
    ax1.set_ylabel('Total Consumption [MWh]', color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    # Plot average temperature on secondary y-axis
    ax2 = ax1.twinx()
    line2, = ax2.plot(temp_days, avg_temp, marker='.', linestyle='-', label='Temperature [°C]', color='tab:orange')
    line2_avg, = ax2.plot(avg_days, avg_temperature, marker=None, linestyle='--', label='Avg Temperature [°C] (all years)', color='tab:orange', alpha=0.5)
    ax2.set_ylabel('Temperature [°C]', color='tab:orange')
    ax2.tick_params(axis='y', labelcolor='tab:orange')

    # Format x-axis as year-month-day, auto-adjust for multiple years
    import matplotlib.dates as mdates
    ax1.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')

    # Combine legends
    lines = [line1, line1_avg, line2, line2_avg]
    labels = [
        'Consumption [MWh]',
        'Avg Consumption [MWh] (all years)',
        'Temperature [°C]',
        'Avg Temperature [°C] (all years)'
    ]
    ax1.legend(lines, labels)

    plt.title('Total Consumption per Day and Weather (All Years) with Daily Averages')
    plt.tight_layout()

    # Save the plot to the outputs folder
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'outputs')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'consumption_temperature_daily.png')
    plt.savefig(output_path)

    #plt.show()


def show_hourly_winter_data(database):
    """
    Plots total consumption and average temperature per hour for the 3rd week of the year 2023,
    and also shows the average per-hour values for all 3rd weeks across all years.
    Saves the plot as a picture in the outputs folder.

    :param database: Database object with required query methods
    """

    results = database.get_consumption_per_hour()
    results_temp = database.get_average_temperature_per_hour()

    # Use datetime objects for direct timeline on x-axis
    hours = [datetime.datetime(row[0], row[1], row[2], row[3]) for row in results]
    consumption = [row[4] for row in results]

    temp_hours = [datetime.datetime(row[0], row[1], row[2], row[3]) for row in results_temp]
    avg_temp = [row[4] for row in results_temp]

    # Filter for only the 3rd week of the year 2023 (ISO week 3)
    filtered = [(dt, cons) for dt, cons in zip(hours, consumption) if dt.isocalendar()[1] == 3 and dt.year == 2023]
    filtered_temp = [(dt, temp) for dt, temp in zip(temp_hours, avg_temp) if dt.isocalendar()[1] == 3 and dt.year == 2023]

    if not filtered or not filtered_temp:
        print("No data for the 3rd week of the year 2023.")
        return

    hours_2023, consumption_2023 = zip(*filtered)
    temp_hours_2023, avg_temp_2023 = zip(*filtered_temp)

    # Calculate average per-hour values for all 3rd weeks across all years
    hour_of_week_consumption = defaultdict(list)
    hour_of_week_temp = defaultdict(list)

    for dt, cons in zip(hours, consumption):
        if dt.isocalendar()[1] == 3:
            hour_of_week = (dt.weekday(), dt.hour)
            hour_of_week_consumption[hour_of_week].append(cons)

    for dt, temp in zip(temp_hours, avg_temp):
        if dt.isocalendar()[1] == 3:
            hour_of_week = (dt.weekday(), dt.hour)
            hour_of_week_temp[hour_of_week].append(temp)

    # Prepare average series for plotting
    # Build a timeline for the 3rd week of 2023
    week_start = min(hours_2023)
    avg_consumption_series = []
    avg_temp_series = []
    avg_time_series = []

    for dt in hours_2023:
        hour_of_week = (dt.weekday(), dt.hour)
        avg_c = np.mean(hour_of_week_consumption[hour_of_week]) if hour_of_week in hour_of_week_consumption else np.nan
        avg_t = np.mean(hour_of_week_temp[hour_of_week]) if hour_of_week in hour_of_week_temp else np.nan
        avg_consumption_series.append(avg_c)
        avg_temp_series.append(avg_t)
        avg_time_series.append(dt)

    plt.figure(figsize=(18, 6))
    ax1 = plt.gca()

    # Plot total consumption
    line1, = ax1.plot(hours_2023, consumption_2023, marker='.', linestyle='-', label='Consumption [MWh] (2023)', color='tab:blue')
    # Plot average consumption
    line1_avg, = ax1.plot(avg_time_series, avg_consumption_series, marker=None, linestyle='--', label='Avg Consumption [MWh] (all years)', color='tab:blue', alpha=0.5)
    ax1.set_xlabel('Date (Year-Month-Day Hour)')
    ax1.set_ylabel('Total Consumption [MWh]', color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    # Plot average temperature on secondary y-axis
    ax2 = ax1.twinx()
    line2, = ax2.plot(temp_hours_2023, avg_temp_2023, marker='.', linestyle='-', label='Temperature [°C] (2023)', color='tab:orange')
    line2_avg, = ax2.plot(avg_time_series, avg_temp_series, marker=None, linestyle='--', label='Avg Temperature [°C] (all years)', color='tab:orange', alpha=0.5)
    ax2.set_ylabel('Temperature [°C]', color='tab:orange')
    ax2.tick_params(axis='y', labelcolor='tab:orange')

    # Format x-axis: one day interval
    import matplotlib.dates as mdates
    locator = mdates.DayLocator()
    formatter = mdates.DateFormatter('%Y-%m-%d %H')
    ax1.xaxis.set_major_locator(locator)
    ax1.xaxis.set_major_formatter(formatter)
    plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')

    # Combine legends
    lines = [line1, line1_avg, line2, line2_avg]
    labels = [
        'Consumption [MWh] (2023)',
        'Avg Consumption [MWh] (all years)',
        'Temperature [°C] (2023)',
        'Avg Temperature [°C] (all years)'
    ]
    ax1.legend(lines, labels)

    plt.title('Total Consumption per Hour and Weather (3rd Week of 2023) with Average of All Years')
    plt.tight_layout()

    # Save the plot to the outputs folder
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'outputs')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'consumption_temperature_hourly_week3_2023.png')
    plt.savefig(output_path)

    #plt.show()


def show_hourly_summer_data(database):
    """
    Plots total consumption and average temperature per hour for the 28th week of the year 2023.
    Saves the plot as a picture in the outputs folder.

    :param database: Database object with required query methods
    """

    results = database.get_consumption_per_hour()
    results_temp = database.get_average_temperature_per_hour()

    # Use datetime objects for direct timeline on x-axis
    hours = [datetime.datetime(row[0], row[1], row[2], row[3]) for row in results]
    consumption = [row[4] for row in results]

    temp_hours = [datetime.datetime(row[0], row[1], row[2], row[3]) for row in results_temp]
    avg_temp = [row[4] for row in results_temp]

    # Filter for only the 28th week of the year 2023 (ISO week 28)
    filtered = [(dt, cons) for dt, cons in zip(hours, consumption) if dt.isocalendar()[1] == 28 and dt.year == 2023]
    filtered_temp = [(dt, temp) for dt, temp in zip(temp_hours, avg_temp) if dt.isocalendar()[1] == 28 and dt.year == 2023]

    if not filtered or not filtered_temp:
        print("No data for the 28th week of the year 2023.")
        return

    hours_2023, consumption_2023 = zip(*filtered)
    temp_hours_2023, avg_temp_2023 = zip(*filtered_temp)

    plt.figure(figsize=(18, 6))
    ax1 = plt.gca()

    # Plot total consumption
    line1, = ax1.plot(hours_2023, consumption_2023, marker='.', linestyle='-', label='Consumption [MWh] (2023)', color='tab:blue')
    ax1.set_xlabel('Date (Year-Month-Day Hour)')
    ax1.set_ylabel('Total Consumption [MWh]', color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    # Plot average temperature on secondary y-axis
    ax2 = ax1.twinx()
    line2, = ax2.plot(temp_hours_2023, avg_temp_2023, marker='.', linestyle='-', label='Temperature [°C] (2023)', color='tab:orange')
    ax2.set_ylabel('Temperature [°C]', color='tab:orange')
    ax2.tick_params(axis='y', labelcolor='tab:orange')

    # Format x-axis: one day interval
    import matplotlib.dates as mdates
    locator = mdates.DayLocator()
    formatter = mdates.DateFormatter('%Y-%m-%d %H')
    ax1.xaxis.set_major_locator(locator)
    ax1.xaxis.set_major_formatter(formatter)
    plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')

    # Combine legends
    lines = [line1, line2]
    labels = [
        'Consumption [MWh] (2023)',
        'Temperature [°C] (2023)'
    ]
    ax1.legend(lines, labels)

    plt.title('Total Consumption per Hour and Weather (28th Week of 2023)')
    plt.tight_layout()

    # Save the plot to the outputs folder
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'outputs')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'consumption_temperature_hourly_week28_2023.png')
    plt.savefig(output_path)

    #plt.show()


def show_hourly_winter_workday_data(database):
    """
    Plots total consumption and average temperature per hour for a single winter workday (Monday) in January 2023,
    and also shows the average per-hour values for all Mondays in January across all years.
    Saves the plot as a picture in the outputs folder.

    :param database: Database object with required query methods
    """

    results = database.get_consumption_per_hour()
    results_temp = database.get_average_temperature_per_hour()

    # Use datetime objects for direct timeline on x-axis
    hours = [datetime.datetime(row[0], row[1], row[2], row[3]) for row in results]
    consumption = [row[4] for row in results]

    temp_hours = [datetime.datetime(row[0], row[1], row[2], row[3]) for row in results_temp]
    avg_temp = [row[4] for row in results_temp]

    # Filter for only the first Monday in January 2023
    filtered = [(dt, cons) for dt, cons in zip(hours, consumption)
                if dt.year == 2023 and dt.month == 1 and dt.weekday() == 0]
    filtered_temp = [(dt, temp) for dt, temp in zip(temp_hours, avg_temp)
                     if dt.year == 2023 and dt.month == 1 and dt.weekday() == 0]

    if not filtered or not filtered_temp:
        print("No data for a winter workday (Monday) in January 2023.")
        return

    # Pick the first Monday (or you can change to another if needed)
    first_monday = min(dt for dt, _ in filtered)
    hours_2023 = [dt for dt, _ in filtered if dt.date() == first_monday.date()]
    consumption_2023 = [cons for dt, cons in filtered if dt.date() == first_monday.date()]
    temp_hours_2023 = [dt for dt, _ in filtered_temp if dt.date() == first_monday.date()]
    avg_temp_2023 = [temp for dt, temp in filtered_temp if dt.date() == first_monday.date()]

    # Calculate average per-hour values for all Mondays in January across all years
    hour_of_day_consumption = defaultdict(list)
    hour_of_day_temp = defaultdict(list)

    for dt, cons in zip(hours, consumption):
        if dt.month == 1 and dt.weekday() == 0:
            hour_of_day_consumption[dt.hour].append(cons)

    for dt, temp in zip(temp_hours, avg_temp):
        if dt.month == 1 and dt.weekday() == 0:
            hour_of_day_temp[dt.hour].append(temp)

    # Prepare average series for plotting
    avg_consumption_series = []
    avg_temp_series = []
    avg_time_series = []

    for dt in hours_2023:
        hour = dt.hour
        avg_c = np.mean(hour_of_day_consumption[hour]) if hour in hour_of_day_consumption else np.nan
        avg_t = np.mean(hour_of_day_temp[hour]) if hour in hour_of_day_temp else np.nan
        avg_consumption_series.append(avg_c)
        avg_temp_series.append(avg_t)
        avg_time_series.append(dt)

    plt.figure(figsize=(14, 6))
    ax1 = plt.gca()

    # Plot total consumption
    line1, = ax1.plot(hours_2023, consumption_2023, marker='.', linestyle='-', label='Consumption [MWh] (Monday, Jan 2023)', color='tab:blue')
    # Plot average consumption
    line1_avg, = ax1.plot(avg_time_series, avg_consumption_series, marker=None, linestyle='--', label='Avg Consumption [MWh] (all Mondays, Jan)', color='tab:blue', alpha=0.5)
    ax1.set_xlabel('Hour')
    ax1.set_ylabel('Total Consumption [MWh]', color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    # Plot average temperature on secondary y-axis
    ax2 = ax1.twinx()
    line2, = ax2.plot(temp_hours_2023, avg_temp_2023, marker='.', linestyle='-', label='Temperature [°C] (Monday, Jan 2023)', color='tab:orange')
    line2_avg, = ax2.plot(avg_time_series, avg_temp_series, marker=None, linestyle='--', label='Avg Temperature [°C] (all Mondays, Jan)', color='tab:orange', alpha=0.5)
    ax2.set_ylabel('Temperature [°C]', color='tab:orange')
    ax2.tick_params(axis='y', labelcolor='tab:orange')

    # Format x-axis: hour interval
    import matplotlib.dates as mdates
    locator = mdates.HourLocator()
    formatter = mdates.DateFormatter('%H:%M')
    ax1.xaxis.set_major_locator(locator)
    ax1.xaxis.set_major_formatter(formatter)
    plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')

    # Combine legends
    lines = [line1, line1_avg, line2, line2_avg]
    labels = [
        'Consumption [MWh] (Monday, Jan 2023)',
        'Avg Consumption [MWh] (all Mondays, Jan)',
        'Temperature [°C] (Monday, Jan 2023)',
        'Avg Temperature [°C] (all Mondays, Jan)'
    ]
    ax1.legend(lines, labels)

    plt.title('Total Consumption per Hour and Weather (First Monday of January 2023) with Average of All Mondays in January')
    plt.tight_layout()

    # Save the plot to the outputs folder
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'outputs')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'consumption_temperature_hourly_first_monday_jan2023.png')
    plt.savefig(output_path)

    #plt.show()

def show_hourly_summer_workday_data(database):
    """
    Plots total consumption and average temperature per hour for a single workday (Monday) in June 2023,
    and also shows the average per-hour values for all Mondays in June across all years.
    Saves the plot as a picture in the outputs folder.

    :param database: Database object with required query methods
    """

    results = database.get_consumption_per_hour()
    results_temp = database.get_average_temperature_per_hour()

    # Use datetime objects for direct timeline on x-axis
    hours = [datetime.datetime(row[0], row[1], row[2], row[3]) for row in results]
    consumption = [row[4] for row in results]

    temp_hours = [datetime.datetime(row[0], row[1], row[2], row[3]) for row in results_temp]
    avg_temp = [row[4] for row in results_temp]

    # Filter for only the Mondays in June 2023
    filtered = [(dt, cons) for dt, cons in zip(hours, consumption)
                if dt.year == 2023 and dt.month == 6 and dt.weekday() == 0]
    filtered_temp = [(dt, temp) for dt, temp in zip(temp_hours, avg_temp)
                        if dt.year == 2023 and dt.month == 6 and dt.weekday() == 0]

    if not filtered or not filtered_temp:
        print("No data for a summer workday (Monday) in June 2023.")
        return

    # Pick the first Monday (or you can change to another if needed)
    first_monday = min(dt for dt, _ in filtered)
    hours_2023 = [dt for dt, _ in filtered if dt.date() == first_monday.date()]
    consumption_2023 = [cons for dt, cons in filtered if dt.date() == first_monday.date()]
    temp_hours_2023 = [dt for dt, _ in filtered_temp if dt.date() == first_monday.date()]
    avg_temp_2023 = [temp for dt, temp in filtered_temp if dt.date() == first_monday.date()]

    # Calculate average per-hour values for all Mondays in June across all years
    hour_of_day_consumption = defaultdict(list)
    hour_of_day_temp = defaultdict(list)

    for dt, cons in zip(hours, consumption):
        if dt.month == 6 and dt.weekday() == 0:
            hour_of_day_consumption[dt.hour].append(cons)

    for dt, temp in zip(temp_hours, avg_temp):
        if dt.month == 6 and dt.weekday() == 0:
            hour_of_day_temp[dt.hour].append(temp)

    # Prepare average series for plotting
    avg_consumption_series = []
    avg_temp_series = []
    avg_time_series = []

    for dt in hours_2023:
        hour = dt.hour
        avg_c = np.mean(hour_of_day_consumption[hour]) if hour in hour_of_day_consumption else np.nan
        avg_t = np.mean(hour_of_day_temp[hour]) if hour in hour_of_day_temp else np.nan
        avg_consumption_series.append(avg_c)
        avg_temp_series.append(avg_t)
        avg_time_series.append(dt)

    plt.figure(figsize=(14, 6))
    ax1 = plt.gca()

    # Plot total consumption
    line1, = ax1.plot(hours_2023, consumption_2023, marker='.', linestyle='-', label='Consumption [MWh] (Monday, Jun 2023)', color='tab:blue')
    # Plot average consumption
    line1_avg, = ax1.plot(avg_time_series, avg_consumption_series, marker=None, linestyle='--', label='Avg Consumption [MWh] (all Mondays, Jun)', color='tab:blue', alpha=0.5)
    ax1.set_xlabel('Hour')
    ax1.set_ylabel('Total Consumption [MWh]', color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    # Plot average temperature on secondary y-axis
    ax2 = ax1.twinx()
    line2, = ax2.plot(temp_hours_2023, avg_temp_2023, marker='.', linestyle='-', label='Temperature [°C] (Monday, Jun 2023)', color='tab:orange')
    line2_avg, = ax2.plot(avg_time_series, avg_temp_series, marker=None, linestyle='--', label='Avg Temperature [°C] (all Mondays, Jun)', color='tab:orange', alpha=0.5)
    ax2.set_ylabel('Temperature [°C]', color='tab:orange')
    ax2.tick_params(axis='y', labelcolor='tab:orange')

    # Format x-axis: hour interval
    import matplotlib.dates as mdates
    locator = mdates.HourLocator()
    formatter = mdates.DateFormatter('%H:%M')
    ax1.xaxis.set_major_locator(locator)
    ax1.xaxis.set_major_formatter(formatter)
    plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')

    # Combine legends
    lines = [line1, line1_avg, line2, line2_avg]
    labels = [
        'Consumption [MWh] (Monday, Jun 2023)',
        'Avg Consumption [MWh] (all Mondays, Jun)',
        'Temperature [°C] (Monday, Jun 2023)',
        'Avg Temperature [°C] (all Mondays, Jun)'
    ]
    ax1.legend(lines, labels)

    plt.title('Total Consumption per Hour and Weather (First Monday of June 2023) with Average of All Mondays in June')
    plt.tight_layout()

    # Save the plot to the outputs folder
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'outputs')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'consumption_temperature_hourly_first_monday_jun2023.png')
    plt.savefig(output_path)

    #plt.show()