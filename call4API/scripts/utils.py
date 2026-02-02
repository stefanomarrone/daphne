from datetime import datetime

from call4API.catalog.coordinates_catalog import coordinates_catalog


# function to define a rectangle given lat-lon and region_size
# xMin, yMin, xMax, yMax
def get_region_string(coords, region_size):
    left = coords[0] - region_size / 2
    right = coords[0] + region_size / 2
    top = coords[1] + region_size / 2
    bottom = coords[1] - region_size / 2
    return [left, bottom, right, top]

def define_coordinates(lat, lon, country_name):
    if lat != '' and lon != '':
        return lat, lon
    elif country_name is not None:
        coordinates = coordinates_catalog().get_coordinates(country_name)
        return list(coordinates.values())

def _pct(x):
    try:
        # I valori che vedi (es. 0.000311) sembrano già "percento".
        return f"{float(x):.2f}%"
    except Exception:
        return "-"


def extract_feature_from_configuration(conf):
    board = conf.board
    lat = board['latitude']
    lon = board['longitude']
    start_date = board['fromdate']
    end_date = board['todate']
    weather_feature_to_extract = board['data']
    country_name = board['countryname']
    return lat, lon, start_date, end_date, weather_feature_to_extract, country_name