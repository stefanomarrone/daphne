# Class to store the response from OpenWeatherAPI
from call4API.scripts.date_utils import timestamp_to_date
from typing import List, Dict


class WeatherDataFields:
    def __init__(self, date, main, wind, clouds, weather_description):
        self.date = date
        self.temperature = main['temp']
        self.feels_like = main['feels_like']
        self.pressure = main['pressure']
        self.humidity = main['humidity']
        self.tem_min = main['temp_min']
        self.temp_max = main['temp_max']
        self.wind_speed = wind['speed']
        self.wind_deg = wind['deg']
        self.wind_gust = wind['gust']
        self.clouds = clouds['all']
        self.weather_description = weather_description['description']

    def get_features(self, features: List[str]) -> Dict:
        extracted_features = {}
        for feature in features:
            if feature in dir(self):
                extracted_features[feature] = getattr(self, feature)
        return extracted_features


class WeatherData:
    def __init__(self, data):
        self.cnt = data['cnt']
        self.weather_list: List[WeatherDataFields] = []

        for item in data['list']:
            weather_data = WeatherDataFields(timestamp_to_date(item['dt']), item['main'], item['wind'], item['clouds'],
                                             item['weather'][0])
            self.weather_list.append(weather_data)
