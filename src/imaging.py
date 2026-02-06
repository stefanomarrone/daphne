from legacy_code.call4API.Image.GeeAPI import GeeAPI
from legacy_code.call4API.Image.skyfiApi import Skyfi
from legacy_code.call4API.catalog.image_catalog import image_catalog

def extract_feature_from_configuration(configuration):
    board = configuration.board
    lat = board['latitude']
    lon = board['longitude']
    start_date = board['fromdate']
    end_date = board['todate']
    country_name = board['countryname']
    return lat, lon, start_date, end_date, country_name

def extract_output_folder(configuration):
    return configuration.board['outfolder']

class ImageGrabber:
    def __init__(self, features):
        pass
        self.features = features
        self.catalog = image_catalog()

class GeeImageGrubber:
    def __init__(self, configuration, gee_api: GeeAPI):
        self.configuration = configuration
        self.gee = gee_api

    def grub(self, configuration):
        lat, lon, start_date, end_date, country_name = extract_feature_from_configuration(configuration)
        output_folder = extract_output_folder(configuration)
        for image_catalog_name, strategy in self.gee.strategies.items():
            self.gee.download_satellite_image(country_name, lat, lon, start_date, end_date, image_catalog_name, strategy, output_folder)


class SkifyImageGrubber:
    def __init__(self, configuration):
        self.configuration = configuration
        self.skify = Skyfi(configuration)

    def grub(self, configuration):
        #self.skify.get_catalog
        #self.skify.place_orders(primi 5 elementi di catalog)
        #self.skyfi.get_order_status(dei 5 ordini) se lo stato è PROCESSING_COMPLETE allora
        #self.skyfi.download_deliverable(id)
        pass


class NoImageGrubber:
    def __init__(self, configuration):
        pass

    def grub(self, configuration):
        pass
