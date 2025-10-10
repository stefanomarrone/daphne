import logging
import httpx
from call4API.Image.GeeAPI import GeeAPI
from dotenv import load_dotenv
import os

from call4API.Image.skyfi import Skyfi

if __name__ == '__main__':
    country_name = "Namibia"
    sky = Skyfi(country_name)
    sky.get_current_user()
    #todo dati da acquisire tramite configurazione - per adesso metto gli esempi in modo da ricordare che formato devono avere

    fromDate = "2023-01-01 00:00:00"
    toDate = "2023-03-01 00:00:00"
    #resolutions = ["LOW", "MEDIUM", "HIGH", "VERY_HIGH"]
    resolutions = ["LOW"]
    productTypes = ["DAY", "MULTISPECTRAL", "SAR"]
    providers = ["SATELLOGIC", "SENTINEL2_CREODIAS", "SIWEI", "UMBRA"]
    catalog_response = sky.get_catalog(country_name, fromDate, toDate, resolutions, productTypes, providers)
    print(catalog_response['archives'])
    sky.save_catalog_gallery(catalog_response['archives'])
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