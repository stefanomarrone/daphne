
class coordinates_catalog:
    def __init__(self):
        self.coordinates_catalogs = {
            "Namibia": {
                "lat": -28.038970,
                "lon": 18.105889
            },
            "Angola":{
                "lat": -16.949631,
                "lon": 12.332528
            },
            "Saudi_Arabia":{
                "lat": 29.6369064,
                "lon": 38.6245267
            },
            "Kenya":{
                "lat": -1.346889,
                "lon": 36.860099
            }
        }

    def get_coordinates(self, country_name):
        return self.coordinates_catalogs[country_name]