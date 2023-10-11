import json

from geojson import FeatureCollection, Feature, Point
from extractors import Extractor
from utils import clean_street_name

# Biedronka data is extracted from Android app. TODO automatic extraction

class BiedronkaExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        with open('extractors/biedronka.json') as file:
            data = json.load(file)

        features = []
        for shop in data:
            if 'Longitude' not in shop:
                continue

            features.append(Feature(
                geometry=Point((shop['Longitude'], shop['Latitude'])),
                properties={
                    'ref': shop['Code'],
                    'name': 'Biedronka',
                    'addr:full': clean_street_name(shop['Street']) if 'Street' in shop else None,
                    'addr:city': shop['City']
                }
            ))

        return FeatureCollection(features)
