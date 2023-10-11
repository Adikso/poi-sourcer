import requests
from geojson import FeatureCollection, Feature, Point
from extractors import Extractor
from utils import clean_street_name


# too free text opening hours
class ZiajaExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('https://ziaja.com/api/ext/wordpress/distribution-points')
        data = response.json()

        features = []
        for shop in data['result']:
            features.append(Feature(
                geometry=Point((shop['lng'], shop['lat'])),
                properties={
                    'name': 'Ziaja',
                    'shop': 'cosmetics',
                    'addr:full': clean_street_name(shop['address']),
                    'addr:city': shop['city'],
                    'addr:postcode': shop['postCode'] if 'postCode' in shop else None,
                    'phone': shop['phone'] if 'phone' in shop else None
                }
            ))

        return FeatureCollection(features)
