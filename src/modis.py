import ee
import requests

from call4API.scripts.utils import change_date_format
from src.catalog.imagecatalog import ImageCatalog
from src.satellite import SatelliteGrabber


class ModisImageGrabber(SatelliteGrabber):
    def __init__(self, features):
        self.catalog_name = "MODIS"
        self.initialise(features)

    def get_visualisations(self, ee_point):
        visualization = {
            'region': ee_point,
            'scale': 30,
            'bands': ['sur_refl_b02', 'sur_refl_b01', 'sur_refl_b03']
        }
        return visualization

    def get_collection(self, ee_point, collection_name, format_s_date, format_e_date):
        collection = ee.ImageCollection(collection_name).filterBounds(ee_point).filterDate(format_s_date, format_e_date).first()
        return collection
