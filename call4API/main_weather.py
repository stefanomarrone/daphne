
from call4API.Data.WeatherAPI import WeatherAPI
from call4API.Data.WeatherData import WeatherData
from call4API.scripts.generate_extracted_data import *

from call4API.scripts.json_utils import *
from src.data import DataGrabber
from dotenv import load_dotenv

lat = -28.038970
lon = 18.105889
start_date = '2023-06-20 12:00:00'
end_date = '2023-06-21 12:00:00'
weather_catalog_name = "OpenWeather"

if __name__ == '__main__':
    load_dotenv()
    api_key = os.getenv('API_KEY')
    weatherAPI = WeatherAPI()
    try:
        # Weather API call
        data = weatherAPI.call_weather_api(lat, lon, start_date, end_date, api_key)
        # folder to store the weather data
        folder_name = create_folder(lat, lon, start_date, end_date, weather_catalog_name)
        # file_path for the JSON weather file
        file_path = generate_json_filepath(folder_name, lat, lon, start_date, end_date, weather_catalog_name)
        # JSON to file
        write_json_to_file(data, file_path)

        #data = read_json_file('/Users/mariastelladebiase/git/repo4pat/call4API/OpenWeather_lat-28.03897_lon18.105889_2024-03-20_12_to_2024-03-21_12/OpenWeather_lat-28.03897_lon18.105889_2024-03-20_12_to_2024-03-21_12.json')

        weather_data = WeatherData(data)

        features_to_extract = ['date', 'temperature', 'humidity', 'pressure']
        data_grabber = DataGrabber(features_to_extract)
        extracted_data = data_grabber.grub(weather_data.weather_list)

        # generate a filename to store the extracted weather data
        extracted_data_file_name = make_filename(folder_name, lat, lon, start_date, end_date, weather_catalog_name)
        # list of weather data to CSV file
        write_dicts_to_csv(extracted_data, extracted_data_file_name)
        #print("Extracted data:", extracted_data)
    except:
        print('try gone wrong')