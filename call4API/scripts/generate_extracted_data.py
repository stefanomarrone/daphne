import os
import csv

from call4API.scripts.utils import date_to_date_hour


def make_filename(extracted_weather_data_dir,lat, lon, start_date, end_date, catalog):
    filename_start = "extracted_weather_data_"
    str_d, str_h = date_to_date_hour(start_date)
    end_d, end_h = date_to_date_hour(end_date)
    filename = os.path.join(
        extracted_weather_data_dir,
        f"{filename_start}_{catalog}_{lat}N_{lon}E_{str_d}-{str_h}_{end_d}-{end_h}.csv"
    )
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
