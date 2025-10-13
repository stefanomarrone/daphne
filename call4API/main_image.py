import logging
import httpx
from call4API.Image.GeeAPI import GeeAPI
from dotenv import load_dotenv
import sys, os
from src.configuration import Configuration
from call4API.Image.skyfi import Skyfi



def skyfi(conf: Configuration):
    sky = Skyfi(conf)
    sky.get_current_user()
    catalog_response = sky.get_catalog()
    sky.save_catalog_gallery(catalog_response['archives'])

functions = {
    'skyfi': skyfi,
}

if __name__ == '__main__':
    configuration = Configuration(sys.argv[1])
    command = functions[sys.argv[2]]
    command(configuration)

'''
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
'''