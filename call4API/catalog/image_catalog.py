
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
            },
            "LANDSAT09": {
                "catalog_name": "USGS_Landsat9_Level2_Collection2_Tier1",
                "collection_name": "LANDSAT/LC09/C02/T1_L2",
                "RGB_bands": ["SR_B4", "SR_B3", "SR_B2"],
                "NIR_band": "SR_B5",
                "min_date": "2021-10-31",
                "max_date": "2024-06-04",
                "resolution": "",
                "ndvi": False
            },
            "LANDSAT08": {
                "catalog_name": "USGS_Landsat8_Collection2_Tier1_RawScenes",
                "collection_name": "LANDSAT/LC08/C02/T1",
                "RGB_bands": ["B4", "B3", "B2"],
                "NIR_band": "B5",
                "min_date": "2013-03-18",
                "max_date": "2024-06-08",
                "resolution": "",
                "ndvi": False
            }
        }

    def get_image_catalog(self, image_catalog_name):
        return self.image_catalogs[image_catalog_name]

    def get_collection_name(self, image_catalog_name):
        return self.image_catalogs[image_catalog_name]['collection_name']
        