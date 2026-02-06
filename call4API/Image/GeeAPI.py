import os

import ee
import requests
from dotenv import load_dotenv

from call4API.catalog.coordinates_catalog import coordinates_catalog
from call4API.catalog.image_catalog import image_catalog
from call4API.scripts.json_utils import create_folder, generate_zip_filepath
from call4API.scripts.utils import get_region_string
from call4API.scripts.date_utils import date_to_date_hour, change_date_format
from abc import ABC, abstractmethod

from mongodb import MongoWriter


class GeeCatalogStrategy(ABC):
    @abstractmethod
    def build_collection(self, catalog: str, ee_point, start_date: str, end_date: str):
        raise NotImplementedError

    @abstractmethod
    def build_download_params(self, ee_point):
        raise NotImplementedError

class ModisStrategy(GeeCatalogStrategy):
    def build_collection(self, catalog, ee_point, start_date, end_date):
        collection = (ee.ImageCollection(catalog)
                      .filterBounds(ee_point)
                      .filterDate(start_date, end_date)
                      .first())
        return ee.Image(collection)

    def build_download_params(self, ee_point):
        return {
            "region": ee_point,
            "scale": 30,
            "bands": ["sur_refl_b02", "sur_refl_b01", "sur_refl_b03"]
        }
class Landsat09Strategy(GeeCatalogStrategy):
    def build_collection(self, catalog, ee_point, start_date, end_date):
        img = (ee.ImageCollection(catalog)
               .filterDate(start_date, end_date)
               .filterBounds(ee_point)
               .map(apply_scale_factors)
               .sort("CLOUD_COVER", True)
               .first())

        ndvi = img.normalizedDifference(["SR_B5", "SR_B4"]).rename(["ndvi"])
        img = img.addBands(ndvi)

        return ee.Image(img)

    def build_download_params(self, ee_point):
        return {
            "region": ee_point,
            "bands": ["SR_B4", "SR_B3", "SR_B2"],
            "min": 0,
            "max": 0.3,
            "scale": 300
        }

def apply_scale_factors(image):
    optical_bands = image.select(['SR_B.']).multiply(0.0000275).add(-0.2)
    thermal_bands = image.select(['ST_B.*']).multiply(0.00341802).add(149)
    return image.addBands(optical_bands, None, True).addBands(thermal_bands, None, True)

def define_coordinates(lat, lon, country_name):
    if lat is not None and lon is not None:
        return lat, lon
    elif country_name is not None:
        coordinates = coordinates_catalog().get_coordinates(country_name)
        return list(coordinates.values())


class GeeAPI():
    def __init__(self, strategies: dict):
        self.catalog = image_catalog()
        self.strategies = strategies

    def inizialize(self):
        load_dotenv()
        project_gee_key = os.getenv('EARTHENGINE_PROJECT')
        ee.Initialize(project=project_gee_key)

    def authenticate(self):
        ee.Authenticate()

    def download_satellite_image(self, country_name, lat, lon, start_date, end_date, image_catalog_name, strategy, output_folder_path):
        self.authenticate()
        self.inizialize()

        c_lt, c_ln = define_coordinates(lat, lon, country_name)
        region = get_region_string([c_ln, c_lt],0.5)
        ee_point = ee.Geometry.Rectangle(region)

        catalog = image_catalog().get_collection_name(image_catalog_name)

        output_folder = create_folder(c_lt, c_ln, country_name, start_date, end_date, image_catalog_name, output_folder_path)
        #print(output_folder)
        image_zip_filepath = generate_zip_filepath(output_folder, c_lt, c_ln, country_name, start_date, end_date, image_catalog_name)


        start_date_fmt, str_h = change_date_format(start_date)
        end_date_fmt, end_h = change_date_format(end_date)

        collection = strategy.build_collection(catalog, ee_point, start_date_fmt, end_date_fmt)
        image = ee.Image(collection)
        visualization = strategy.build_download_params(ee_point)
        url = image.getDownloadUrl(visualization)

        response = requests.get(url)
        with open(image_zip_filepath, 'wb') as f:
            f.write(response.content)
        return image_zip_filepath

    def download_satellite_image_with_assets(self, catalog, ee_point, start_date, end_date, output_folder):
        collection = ee.ImageCollection(catalog) \
            .filterBounds(ee_point) \
            .filterDate(start_date, end_date) \
            .first()
        image = ee.Image(collection)

        task = ee.batch.Export.image.toAsset(image=image, description='image_export',
                                             assetId='projects/ee-stelladebiase/assets/prova', region=ee_point,
                                             scale=30)

        task.start()
        print('Image Downloaded!')
