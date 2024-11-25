
class CoordinateExtractor:
    catalog = {
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
        },
        "default": {
            "lat": 0,
            "lon": 0
        }
    }

    def get_coordinates_from_country(country_name):
        country_to_search = country_name if country_name in CoordinateExtractor.catalog.keys() else "default"
        dictionary_entry = CoordinateExtractor.catalog[country_to_search]
        lat, lon = dictionary_entry["lat"], dictionary_entry["lon"]
        return lat, lon

    def get_coordinates(country_name, latitude, longitude):
        lat = latitude
        lon = longitude
        if (latitude == '') or (longitude == ''):
            lat, lon = CoordinateExtractor.get_coordinates_from_country(country_name)
        return lat, lon