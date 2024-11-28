# Class to implement the get call for different weather API
import requests

from call4API.scripts.date_utils import date_to_timestamp


class WeatherAPI:
    def __init__(self):
        self.catalog = {
            "OpenWeather": 'https://history.openweathermap.org/data/2.5/history/',
            "Gee": ""
        }

    def call_weather_api(self, lat, lon, start, end, api_key, catalog_name="OpenWeather"):

        start_unix = date_to_timestamp(start)
        end_unix = date_to_timestamp(end)
        url = f'{self.catalog[catalog_name]}city?lat={lat}&lon={lon}&type=hour&start={start_unix}&end={end_unix}&units=metric&appid={api_key}'
        # Make a GET request to the API endpoint
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            # Process the data as needed
            #print(data)
            return data
        else:
            # Print an error message if the request was unsuccessful
            print('Error:', response.status_code)
            print('Reason:', response.reason)
            raise Exception('Error')
