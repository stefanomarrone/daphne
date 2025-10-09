import os

import ee
import requests
from dotenv import load_dotenv

from call4API.catalog.coordinates_catalog import coordinates_catalog
from call4API.catalog.image_catalog import image_catalog
from call4API.scripts.json_utils import create_folder, generate_zip_filepath
from call4API.scripts.utils import get_region_string, change_date_format


def define_coordinates(lat, lon, country_name):
    if lat is not None and lon is not None:
        return lat, lon
    elif country_name is not None:
        coordinates = coordinates_catalog().get_coordinates(country_name)
        return list(coordinates.values())


class GeeAPI:
    def __init__(self):
        self.catalog = image_catalog()

    def inizialize(self):
        # Initialize Earth Engine
        load_dotenv()
        project_gee_key = os.getenv('EARTHENGINE_PROJECT')
        ee.Initialize(project=project_gee_key)

    def authenticate(self):
        ee.Authenticate()

    def call_image_api(self, catalog, ee_point, start_date, end_date, image_zip_filepath):
        start_date, str_h = change_date_format(start_date)
        end_date, end_h = change_date_format(end_date)

        # Load a satellite image collection (e.g., Landsat, Modis)
        collection = ee.ImageCollection(catalog) \
            .filterBounds(ee_point) \
            .filterDate(start_date, end_date) \
            .first()

        # Get the first image in the collection
        image = ee.Image(collection)

        # Define the url
        url = image.getDownloadUrl(
            {'region': ee_point, 'scale': 30, 'bands': ['sur_refl_b02', 'sur_refl_b01', 'sur_refl_b03']})

        response = requests.get(url)
        with open(image_zip_filepath, 'wb') as f:
            f.write(response.content)

        # Print a message indicating that the export has started
        print('Exporting image...')

    def download_satellite_image(self, country_name, lat, lon, start_date, end_date, image_catalog_name="MODIS"):
        # Initialize Earth Engine
        self.inizialize()

        c_lt, c_ln = define_coordinates(lat, lon, country_name)

        region = get_region_string([c_ln, c_lt],
                                   0.5)  # [lon, lat] ricorda che gee richiede le coordinate in modo inverso rispetto OPWeather
        ee_point = ee.Geometry.Rectangle(region)

        catalog = image_catalog().get_collection_name(image_catalog_name)

        output_folder = create_folder(c_lt, c_ln, country_name, start_date, end_date,
                                      image_catalog_name)
        print(output_folder)

        image_zip_filepath = generate_zip_filepath(output_folder, c_lt, c_ln, country_name, start_date,
                                                   end_date, image_catalog_name)
        self.call_image_api(catalog, ee_point, start_date, end_date, image_zip_filepath)

    def download_satellite_image_with_assets(self, catalog, ee_point, start_date, end_date, output_folder):
        # Load a satellite image collection (e.g., Landsat, Modis)
        collection = ee.ImageCollection(catalog) \
            .filterBounds(ee_point) \
            .filterDate(start_date, end_date) \
            .first()
        # Get the first image in the collection
        image = ee.Image(collection)

        # Define the export task
        task = ee.batch.Export.image.toAsset(image=image, description='image_export',
                                             assetId='projects/ee-stelladebiase/assets/prova', region=ee_point,
                                             scale=30)

        # Start the export task
        task.start()

        # Print a message indicating that the export task has started
        print('Exporting image...')
