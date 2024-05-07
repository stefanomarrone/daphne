import ee
import requests

from call4API.catalog.image_catalog import image_catalog
from call4API.scripts.json_utils import create_folder, generate_zip_filepath
from call4API.scripts.utils import get_region_string, change_date_format, define_coordinates


def extract_feature_from_configuration(features):
    board = features.board
    lat = board['latitude']
    lon = board['longitude']
    start_date = board['fromdate']
    end_date = board['todate']
    country_name = board['countryname']
    return lat, lon, start_date, end_date, country_name


class ImageGrabber():
    def __init__(self, features):
        pass
        self.features = features
        self.catalog = image_catalog()


class ModisImageGrubber:
    def __init__(self, configuration):
        self.configuration = configuration

    def grub(self, configuration):
        lat, lon, start_date, end_date, country_name \
            = extract_feature_from_configuration(configuration)
        image_catalog_name = "MODIS"

        self.download_satellite_image(country_name, lat, lon, start_date, end_date, image_catalog_name)

    def download_satellite_image(self, country_name, lat, lon, start_date, end_date, image_catalog_name="MODIS"):
        # Initialize Earth Engine
        ee.Initialize()

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

        return print('Exporting complete!')

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
        return print('Exporting image...')


class DummyImageGrubber(ImageGrabber):
    def grub(self):
        print("This is a test. And this is the DummyImageGrubber")


class StupidImageGrubber(ImageGrabber):
    def grub(self):
        print("This is a test. And this is the StupidImageGrubber")
