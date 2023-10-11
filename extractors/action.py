from datetime import datetime

import requests
from geojson import FeatureCollection, Feature, Point

from extractors import Extractor
from utils import is_in_poland


# get data for each store todo
class ActionExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('https://www.action.com/api/stores/coordinates/')
        data = response.json()

        # Api is randomly changing response
        if 'data' in data:
            data = data['data']
        if 'items' in data:
            data = data['items']

        features = []
        for shop in data:
            if not is_in_poland((shop['latitude'], shop['longitude'])):
                continue

            opening_date = datetime.fromisoformat(shop['initialOpeningDate']).strftime("%Y-%m-%d")
            features.append(Feature(
                geometry=Point((float(shop['longitude']), float(shop['latitude']))),
                properties={
                    'ref': shop['branchNumber'],
                    'name': 'Action',
                    'brand': 'Action',
                    'brand:wikidata': 'Q2634111',
                    'shop': 'variety_store',
                    'start_date': opening_date if shop['currentlyOpened'] else None,
                    'opening_date': opening_date if not shop['currentlyOpened'] else None,
                }
            ))

        return FeatureCollection(features)
