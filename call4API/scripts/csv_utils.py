import os
import csv

from call4API.scripts.json_utils import create_filepath


def generate_csv_filepath(folder_name, lat, lon, country_name, start_date, end_date):
    catalog = "extracted_weather_data"
    filepath = create_filepath(folder_name, catalog, lat, lon, country_name, start_date, end_date, 'csv')
    return filepath


# function to generate a csv file in the workspace in a specific folder
def generate_csv_filename(extracted_weather_data_dir, lat, lon, country_name, start_date, end_date):
    csv_filepath = generate_csv_filepath(extracted_weather_data_dir, lat, lon, country_name, start_date, end_date)
    filename = os.path.join(extracted_weather_data_dir, csv_filepath)
    return filename


# function to write the list of weather data from dictionaries to a CSV file.
def write_dicts_to_csv(data, filename):
    # Extract column headers from the keys of the first dictionary in the list
    headers = data[0].keys() if data else []

    # Write data to CSV file
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)

        # Write header row
        writer.writeheader()

        # Write data rows
        writer.writerows(data)
