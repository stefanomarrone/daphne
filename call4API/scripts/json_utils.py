import json
import os

# function to read a JSON.
from call4API.scripts.date_utils import date_to_date_hour, change_date_format


def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


# function to write JSON data to a file.
# json_data (dict or list): The JSON data to be written to the file.
# file_path (str): The path to the file where JSON data will be written.
def write_json_to_file(json_data, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)


# function to generate the filepath of the JSON response of weatherAPI
def generate_json_filepath(folder_name, lat, lon, country_name, start_date, end_date, catalog):
    filepath = create_filepath(folder_name, catalog, lat, lon, country_name, start_date, end_date, 'json')
    return filepath


# function to generate the filepath of the JSON response of weatherAPI
def generate_zip_filepath(folder_name, lat, lon, country_name, start_date, end_date, catalog):
    filepath = create_filepath(folder_name, catalog, lat, lon, country_name, start_date, end_date, 'zip')
    return filepath

# Create a folder in the workspace with a name containing latitude, longitude, start date, end date, and catalog.
def create_folder(lat, lon, country_name, start_date, end_date, catalog):
    str_d, str_h = change_date_format(start_date)
    end_d, end_h = change_date_format(end_date)
    folder_name = create_folder_name(catalog, lat, lon, str_d, str_h, end_d, end_h, country_name)
    # Create the folder in the workspace
    folder_path = os.path.join(os.getcwd(), folder_name)
    os.makedirs(folder_path, exist_ok=True)

    return folder_path


def create_folder_name(catalog, lat, lon, str_d, str_h, end_d, end_h, country_name):
    if lat != '' and lon != '' and country_name == '':
        return f"{catalog}_lat{lat}_lon{lon}_{str_d}_{str_h}_to_{end_d}_{end_h}"
    elif lat != '' and lon != '' and country_name != '':
        return f"{catalog}_{country_name}_lat{lat}_lon{lon}_{str_d}_{str_h}_to_{end_d}_{end_h}"
    else:
        return f"{catalog}_{str_d}_{str_h}_to_{end_d}_{end_h}"


def create_filepath(folder_name, catalog, lat, lon, country_name, start_date, end_date, format):
    str_d, str_h = change_date_format(start_date)
    end_d, end_h = change_date_format(end_date)
    if lat != '' and lon != '' and country_name == '':
        return f"{folder_name}/{catalog}_lat{lat}_lon{lon}_{str_d}_{str_h}_to_{end_d}_{end_h}.{format}"
    elif lat != '' and lon != '' and country_name != '':
        return f"{folder_name}/{catalog}_{country_name}_{str_d}_{str_h}_to_{end_d}_{end_h}.{format}"
    else:
        return f"{folder_name}/{catalog}_{str_d}_{str_h}_to_{end_d}_{end_h}.{format}"
