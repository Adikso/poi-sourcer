import json

import requests
from bs4 import BeautifulSoup
from geojson import FeatureCollection, Feature, Point
from extractors import Extractor
from utils import extract_address_from_text


# todo
class LubaszkaExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('https://www.lubaszka.pl/')
        soup = BeautifulSoup(response.content)
        data = json.loads(soup.select_one('#mapMarkers').text)

        features = []
        for shop in data:
            address_tags = extract_address_from_text(shop[5])

            features.append(Feature(
                geometry=Point((float(shop[4]), float(shop[3]))),
                properties=address_tags | {
                    'brand:wikidata': 'Q108586693',
                    'brand': 'Galeria Wypieków Lubaszka',
                    'name': 'Galeria Wypieków Lubaszka',
                    'alt_name': 'Lubaszka',
                    'addr:full': shop[5],
                    'amenity': 'cafe' if shop[2] == 'Kawiarnia' else None,
                    'shop': 'bakery' if shop[2] == 'Piekarnia' else None
                }
            ))

        return FeatureCollection(features)
