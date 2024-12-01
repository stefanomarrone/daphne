import os
from typing import List

import requests
from dotenv import load_dotenv

from call4API.Data.WeatherData import WeatherDataFields, WeatherData
from call4API.scripts.date_utils import date_to_timestamp
from call4API.scripts.csv_utils import generate_csv_filename, write_dicts_to_csv
from call4API.scripts.json_utils import create_folder, generate_json_filepath, write_json_to_file
from call4API.scripts.utils import define_coordinates


def extract_feature_from_configuration(features):
    board = features.board
    lat = board['latitude']
    lon = board['longitude']
    start_date = board['fromdate']
    end_date = board['todate']
    weather_feature_to_extract = board['data']
    country_name = board['countryname']
    return lat, lon, start_date, end_date, weather_feature_to_extract, country_name


class OPWDataGrabber:
    def __init__(self, features):
        self.catalog_api_url = 'https://history.openweathermap.org/data/2.5/history/'
        self.initialise(features)

    def initialise(self, features):
        self.latitude = features['latitude']
        self.longitude = features['longitude']
        self.start_date = features['fromdate']
        self.end_date = features['todate']
        self.country_name = features['country_name']


    def grab(self, configuration):
        load_dotenv()
        api_key = os.getenv('API_KEY')
        weather_catalog_name = "OpenWeather"

        lat, lon = define_coordinates(self.latitude, self.longitude, self.country_name)
        try:
            # Weather API call
            data = self.call_weather_api(lat, lon, self.start_date, self.end_date, api_key)
            # folder to store the weather data
            folder_name = create_folder(lat, lon, self.country_name, self.start_date, self.end_date, weather_catalog_name)
            # file_path for the JSON weather file
            file_path = generate_json_filepath(folder_name, lat, lon, self.country_name, self.start_date, self.end_date, weather_catalog_name)
            # JSON to file
            write_json_to_file(data, file_path)

            weather_data = WeatherData(data)

            extracted_data = self.extract(weather_data.weather_list)

            # generate a filename to store the extracted weather data
            extracted_data_file_name = generate_csv_filename(folder_name, lat, lon, self.country_name, self.start_date, self.end_date)
            # list of weather data to CSV file
            write_dicts_to_csv(extracted_data, extracted_data_file_name)
            print("Extracted data:", extracted_data)
            print("Extraction data complete!")
            return extracted_data
        except:
            print('OpenWeather try gone wrong')

    def extract(self, data: List[WeatherDataFields]):
        extracted_data = []
        for item in data:
            extracted_data.append(item.get_features(self.configuration.board['data']))
        return extracted_data

    def call_weather_api(self, lat, lon, start, end, api_key):
        start_unix = date_to_timestamp(start)
        end_unix = date_to_timestamp(end)
        url = f'{self.catalog_api_url}city?lat={lat}&lon={lon}&type=hour&start={start_unix}&end={end_unix}&units=metric&appid={api_key}'
        response = requests.get(url)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            # Process the data as needed
            return data
        else:
            print('Error:', response.status_code)
            print('Reason:', response.reason)
            raise Exception('Error')


# other grabber for other services
class LDataGrabber:
    def __init__(self, features):
        self.features = features
		
class MDataGrabber:
    def __init__(self, features):
        self.features = features

class DataGrabber():
    def __init__(self, features):
        pass
        # todo extract single features


class DummyDataGrubber(DataGrabber):
    def grab(self):
        print("This is a test. And this is the DummyDataGrubber")

class StupidDataGrubber(DataGrabber):
    def grab(self):
        print("This is a test. And this is the StupidDataGrubber")
