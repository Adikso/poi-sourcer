import json

import requests
from bs4 import BeautifulSoup
from geojson import FeatureCollection, Feature, Point
from extractors import Extractor

# There are opening dates and address
class OskrobaExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('https://oskroba.pl/znajdz-sklep')
        soup = BeautifulSoup(response.text, 'html.parser')
        json_data = json.loads(soup.select_one('#placesJSON').text)

        features = []
        for shop in json_data:
            features.append(Feature(
                geometry=Point((float(shop['lng']), float(shop['lat']))),
                properties={
                    'ref': shop['id'],
                    'name': 'Oskroba',
                    'shop': 'bakery',
                    'addr:city': shop['city']
                }
            ))

        return FeatureCollection(features)
