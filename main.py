
from src.data_loader import RawData
from src.data_processing import ProcessedData
from src.db_loader import EnergyDataDB
import matplotlib.pyplot as plt

from src.gui import Gui

def collect_data():
    """
    Collects data from various sources and returns a dictionary containing the data.
    """
    print("\nStarting data processing...")
    raw_data = RawData()
    print("Raw data collected successfully.\n")

    return raw_data

def process_data(raw_data):
    """
    Collects and processes data, then returns the processed data object.
    """
    print("Processing raw data...")
    processed_data = ProcessedData(raw_data)
    print("Raw data processed successfully.\n")

    return processed_data

def show_data(results_list, labels, xlabel, ylabel, title):
    """
    Plots multiple results on the same graph.

    :param results_list: List of results, each result is a list of tuples (e.g., from DB queries)
    :param labels: List of labels for each result set
    :param xlabel: Label for the x-axis
    :param ylabel: Label for the y-axis
    :param title: Title of the plot
    """
    plt.figure(figsize=(10, 5))
    ax1 = plt.gca()

    # Plot the first dataset on the primary y-axis
    months = [row[1] for row in results_list[0]]
    y1 = [row[2] for row in results_list[0]]
    line1, = ax1.plot(months, y1, marker='o', label=labels[0], color='tab:blue')
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel, color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    # If there is a second dataset, plot it on a secondary y-axis
    if len(results_list) > 1:
        ax2 = ax1.twinx()
        months2 = [row[1] for row in results_list[1]]
        y2 = [row[2] for row in results_list[1]]
        line2, = ax2.plot(months2, y2, marker='o', label=labels[1], color='tab:orange')
        ax2.set_ylabel(labels[1], color='tab:orange')
        ax2.tick_params(axis='y', labelcolor='tab:orange')
        lines = [line1, line2]
        labels_combined = [labels[0], labels[1]]
        ax1.legend(lines, labels_combined)
    else:
        ax1.legend([line1], [labels[0]])

    plt.title(title)
    plt.xticks(months)
    plt.tight_layout()
    plt.show()

def analyze_data():
    """
    Analyzes the processed data and returns the analysis results.
    """
    print("Analyzing processed data...")
    database = EnergyDataDB()
    results_23 = database.get_consumption_per_month(year=2023)
    results_23_temp = database.get_average_temperature_per_month(year=2023)
    show_data([results_23, results_23_temp], ['Consumption [MWh]', 'Temperature [°C]'], 'Month', 'Total Consumption', 'Total Consumption per Month and Weather in 2023')


    # Extract months and consumption values

    


def main():
    raw_data = collect_data()
    process_data(raw_data)
    analyze_data()


if __name__ == "__main__":
    main()
    gui = Gui()
    #gui.run()

