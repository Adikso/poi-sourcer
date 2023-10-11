import requests
from geojson import FeatureCollection, Feature, Point
from extractors import Extractor


class EpakaExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('https://www.epaka.pl/punkt/aj_markers')
        data = response.json()

        features = []
        for shop in data:
            if not shop['longitude'] or not shop['latitude']:
                continue

            features.append(Feature(
                geometry=Point((float(shop['longitude']), float(shop['latitude']))),
                properties={
                    'ref': shop['id'],
                    'name': 'epaka.pl',
                    'amenity': 'post_office',
                    'addr:city': shop['miasto'],
                }
            ))

        return FeatureCollection(features)
