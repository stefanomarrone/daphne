
from call4API.Image.GeeAPI import GeeAPI
from dotenv import load_dotenv
import os

if __name__ == '__main__':

    lat = -16.949631
    lon = 12.332528
    #lat = None
    #lon = None
    start_date = "2023-01-01 12:00:00"
    end_date = "2023-01-02 12:00:00"
    image_catalog_name = "MODIS"
    #country_name = "Saudi_Arabia"
    country_name = ''


    geeAPI = GeeAPI()
    geeAPI.authenticate()
    geeAPI.download_satellite_image(country_name, lat, lon, start_date, end_date, image_catalog_name)
    load_dotenv()
    skyfi_key = os.getenv('API_KEY_SKYFI')