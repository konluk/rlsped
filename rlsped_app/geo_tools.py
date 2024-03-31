import time
import math
from geopy.distance import geodesic
from geopy.geocoders import Nominatim


class GeoTools:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="zip_code_distance_calculator")


    def get_location_info(self, zip_code):
        zip_code = self.fix_zip_code(zip_code)

        for x in range(3):
            try:
                location = self.geolocator.geocode(zip_code)
                break
            except Exception as e:
                print(e)
                time.sleep(1)
        else:
            raise Exception("PROBLEM WITH CONNECTION, TRY LATER.")

        if location is None:
            raise Exception("ZIP: %s CODE NOT FOUND!" % zip_code)

        location_city = location.raw.get('display_name').split(",")
        location_city = location_city[1].strip() + "/" + location_city[2].strip()

        return location.latitude, location.longitude, location_city

    @staticmethod
    def fix_zip_code(zip_code):
        zip_code = zip_code.strip()
        if not zip_code[0].isalpha():
            raise Exception("FIRST CHARACTER IN ZIP CODE MUST BE LETTER!")

        if len(zip_code) < 4:
            raise Exception("ZIP CODE MUST HAVE MORE THEN 3 CHARACTERS")

        if zip_code[2] != " ":
            zip_code = zip_code[:2] + " " + zip_code[2:]

        return zip_code

    def haversine(self, lat1, lon1, lat2, lon2):
        lat1, lon1, lat2, lon2 = float(lat1), float(lon1), float(lat2), float(lon2)

        R = 6371  # Radius of the Earth in kilometers

        # Convert latitude and longitude from degrees to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c

        return distance
