import ee
import requests

from call4API.scripts.json_utils import create_folder, generate_zip_filepath
from call4API.scripts.utils import get_region_string, change_date_format
from src.utils import define_coordinates
from src.catalog.imagecatalog import ImageCatalog
from src.satellite import SatelliteGrabber


class LandsatImageGrubber(SatelliteGrabber):
    def __init__(self, features, catalog_name):
        self.initialise(features)
        self.catalog_name = catalog_name

    def apply_scale_factors(self, image):
        # Applicazione dei fattori di scala per le bande ottiche
        optical_bands = image.select(['SR_B.']).multiply(0.0000275).add(-0.2)
        # Applicazione dei fattori di scala per le bande termiche
        thermal_bands = image.select(['ST_B.*']).multiply(0.00341802).add(149)
        # Aggiunta delle bande ottiche e termiche all'immagine
        return image.addBands(optical_bands, None, True).addBands(thermal_bands, None, True)

    def get_visualisations(self, ee_point):
        visualization = {
            'bands': ['SR_B4', 'SR_B3', 'SR_B2'],
            'min': 0,
            'max': 0.3,
            'scale': 300
        }
        return visualization

    def get_collection(self, ee_point, collection_name, format_s_date, format_e_date):
        collection = ee.ImageCollection(collection_name).filterDate(format_s_date, format_e_date) \
            .filterBounds(ee_point) \
            .map(self.apply_scale_factors) \
            .sort('CLOUD_COVER', True) \
            .first()
        ndvi = collection.normalizedDifference(['SR_B5', 'SR_B4']).rename(['ndvi'])
        images = collection.addBands(ndvi)  # TODO: capire a cosa serve images
        return collection
