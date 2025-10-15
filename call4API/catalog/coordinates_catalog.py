
class coordinates_catalog:
    def __init__(self):
        self.coordinates_catalogs = {
            "Namibia": {
                "lat": -28.038970,
                "lon": 18.105889
            },
            "Namibia_Desert": {
                "lat": -26.6446901,
                "lon": 16.0803984
            },
            "Namibia_Savanna": {
                "lat": -24.9229818,
                "lon": 15.8887668
            },
            "Angola": {
                "lat": -16.949631,
                "lon": 12.332528
            },
            "Saudi_Arabia": {
                "lat": 29.6369064,
                "lon": 38.6245267
            },
            "Kenya": {
                "lat": -1.346889,
                "lon": 36.860099
            },
            "Australia_Mulga": {
                "lat": -23.5358481,
                "lon": 119.8517412
            },
            "Australia_Western": {
                "lat": -23.4186270,
                "lon": 119.8371248
            },
            "Australia_Western_Mulga": {
                "lat": -23.360976,
                "lon": 19.955787
            },
            "Niger": {
                "lat": 15.7289412,
                "lon": 9.0080611
            },
            "Niger_Savanna": {
                "lat": 16.6374777,
                "lon": 6.2709376
            },
            "Chad": {
                "lat": 15.827323,
                "lon": 20.147305
            }
        }

    def get_coordinates(self, country_name):
        return self.coordinates_catalogs[country_name]

    def get_countryname(self, lat: float, lon: float):
        for name, coords in self.coordinates_catalogs.items():
            if coords["lat"] == lat and coords["lon"] == lon:
                return name
            else:
                return None