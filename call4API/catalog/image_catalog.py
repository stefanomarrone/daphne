
class image_catalog:
    def __init__(self):

        self.image_catalogs = {
            "MODIS": {
                "catalog_name": "MOD13Q1.061",
                "collection_name": "MODIS/061/MOD13Q1",
                "RGB_bands": ["sur_refl_b01", "sur_refl_b03"],
                "NIR_band": "sur_refl_b02",
                "min_date": "2000-02-18",
                "max_date": "2024-04-06",
                "resolution": "250m",
                "ndvi": True
            }
        }

    def get_image_catalog(self, image_catalog_name):
        return self.image_catalogs[image_catalog_name]

    def get_collection_name(self, image_catalog_name):
        return self.image_catalogs[image_catalog_name]['collection_name']
        