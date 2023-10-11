import requests
from geojson import FeatureCollection, Feature, Point
from extractors import Extractor


class LewiatanExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('https://lewiatan.pl/api/stores')
        data = response.json()

        features = []
        for shop in data['data']:
            features.append(Feature(
                geometry=Point((float(shop['longitude']), float(shop['latitude']))),
                properties={
                    'name': 'Lewiatan',
                    'brand': 'Lewiatan',
                    'shop': 'supermarket',
                    'addr:full': shop['address'],
                    'addr:city': shop['city'],
                    'addr:postcode': shop['post_code'],
                    'phone': shop['phone'],
                    'website': 'https://lewiatan.pl' + shop['url']
                }
            ))

        return FeatureCollection(features)
