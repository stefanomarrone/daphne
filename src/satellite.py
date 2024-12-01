import ee
import requests

from call4API.scripts.json_utils import create_folder, generate_zip_filepath
from call4API.scripts.utils import get_region_string, change_date_format
from src.utils import define_coordinates
from src.catalog.imagecatalog import ImageCatalog
from src.imaging import ImageGrabber


class SatelliteGrabber(ImageGrabber):
    def __init__(self, features):
        self.catalog_name = None
        self.initialise(features)

    def initialise(self, features):
        self.latitude = features['latitude']
        self.longitude = features['longitude']
        self.start_date = features['fromdate']
        self.end_date = features['todate']
        self.country_name = features['country_name']
        self.catalog = ImageCatalog(self.catalog_name)

    def grab(self):
        # Initialize Earth Engine
        ee.Initialize(project='mat4pat')
        c_lt, c_ln = define_coordinates(self.latitude, self.longitude, self.country_name)
        region = get_region_string([c_ln, c_lt],0.5)  # [lon, lat] ricorda che gee richiede le coordinate in modo inverso rispetto OPWeather
        ee_point = ee.Geometry.Rectangle(region)
        output_folder = create_folder(c_lt, c_ln, self.country_name, self.start_date, self.end_date, self.catalog_name)
        print(output_folder)
        image_zip_filepath = generate_zip_filepath(output_folder, c_lt, c_ln, self.country_name, self.start_date, self.end_date, self.catalog_name)
        self.call_image_api(ee_point, image_zip_filepath)
        print('Exporting complete!')

    def call_image_api(self, ee_point, image_zip_filepath):
        collection_name = ImageCatalog(self.catalog_name).get_collection_name()
        formatted_start_date, _ = change_date_format(self.start_date)
        formatted_end_date, _ = change_date_format(self.end_date)
        # Load a satellite image collection (e.g., Landsat, Modis)
        collection = self.get_collection(ee_point, collection_name, formatted_start_date, formatted_end_date)
        # Define the visualisation dictionary
        visualization = self.get_visualisations(ee_point)
        image = ee.Image(collection)
        url = image.getDownloadUrl(visualization)
        response = requests.get(url)
        with open(image_zip_filepath, 'wb') as f:
            f.write(response.content)
        # Print a message indicating that the export has started
        print('Exporting image...')



