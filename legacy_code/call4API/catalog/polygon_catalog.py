from shapely.geometry import Point, Polygon
from shapely.ops import transform
from pyproj import Transformer
import math

class polygon_catalog:
    def __init__(self):
        self.polygon_catalog = {
            "Namibia": "POLYGON ((18.093147 -28.049749, 18.118039 -28.050274, 18.118628 -28.02819, 18.093741 -28.027665, 18.093147 -28.049749))",
            "Angola":"POLYGON((12.321896 -16.959589, 12.342875 -16.959863, 12.343159 -16.939672, 12.322182 -16.939398, 12.321896 -16.959589))",
            "Saudi_Arabia": "POLYGON((38.613015 29.626783, 38.636113 29.626848, 38.636040 29.647029, 38.612938 29.646963, 38.613015 29.626783))",
            "Kenya": "POLYGON((36.850047 -1.356988, 36.870133 -1.357006, 36.870151 -1.336790, 36.850065 -1.336772, 36.850047 -1.356988))"
        }

    def get_polygon_catalog(self, country_name):
        return self.polygon_catalog[country_name]

    def create_polygon(self, lat: float, lon: float) -> str:
        #Crea un poligono quadrato di circa 5 km² centrato su una coordinata (lat, lon).
        target_area_km2 = 6.0
        side_m = math.sqrt(target_area_km2 * 1_000_000)  # ~2236.07 m
        half_side = side_m / 2

        utm_zone = int(math.floor((lon + 180) / 6) + 1)
        epsg = f"EPSG:{32600 + utm_zone if lat >= 0 else 32700 + utm_zone}"

        to_utm = Transformer.from_crs("EPSG:4326", epsg, always_xy=True).transform
        to_wgs = Transformer.from_crs(epsg, "EPSG:4326", always_xy=True).transform

        p_utm = transform(to_utm, Point(lon, lat))

        x, y = p_utm.x, p_utm.y
        square = Polygon([
            (x - half_side, y - half_side),
            (x + half_side, y - half_side),
            (x + half_side, y + half_side),
            (x - half_side, y + half_side),
            (x - half_side, y - half_side)
        ])

        square_wgs = transform(to_wgs, square)

        coords = ", ".join([f"{lon:.6f} {lat:.6f}" for lon, lat in square_wgs.exterior.coords])
        return f"POLYGON(({coords}))"
