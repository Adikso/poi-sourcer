import json

import requests
from bs4 import BeautifulSoup
from geojson import FeatureCollection, Feature, Point
from extractors import Extractor
from utils import extract_address_from_text


class PekaoSAExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('https://www.pekao.com.pl/.rest/branches')
        data = response.json()

        features = []
        for shop in data:
            features.append(Feature(
                geometry=Point((float(shop['lg']), float(shop['lt']))),
                properties={
                    'ref': shop['branchItemId']
                }
            ))

        return FeatureCollection(features)
