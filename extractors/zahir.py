import requests
from geojson import FeatureCollection, Feature, Point
from extractors import Extractor
from utils import extract_js_var_from_html


# jest adres w głupim formacie
class ZahirExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('https://zahirkebab.pl/lokale/')
        data = extract_js_var_from_html(response.content, 'umsAllMapsInfo')

        features = []
        for shop in data[0]['markers']:
            features.append(Feature(
                geometry=Point((float(shop['coord_y']), float(shop['coord_x']))),
                properties={
                    'name': 'Zahir Kebab',
                    'cuisine': 'kebab',
                    'amenity': 'fast_food',
                }
            ))

        return FeatureCollection(features)
