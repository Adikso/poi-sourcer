import requests
from geojson import FeatureCollection, Feature, Point
from extractors import Extractor
from utils import extract_js_var_from_html


# todo address
class TopazExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('https://topaz24.pl/sklepy-topaz')
        data = extract_js_var_from_html(response.text, 'locations')

        features = []
        for shop in data:
            features.append(Feature(
                geometry=Point((float(shop[3]), float(shop[2]))),
                properties={
                    'name': 'Topaz'
                }
            ))

        return FeatureCollection(features)
