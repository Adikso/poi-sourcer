import requests
from geojson import FeatureCollection, Feature, Point
from extractors import Extractor
from utils import clean_street_name
from utils.opening_dates import create_from_freetext


class VisionExpressExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('https://visionexpress.pl/poses', headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0'
        })
        data = response.json()

        features = []
        for shop in data['poses']:
            features.append(Feature(
                geometry=Point((shop['longitude'], shop['latitude'])),
                properties={
                    'ref': shop['name'],
                    'brand:wikidata': 'Q7936150',
                    'name': 'Vision Express',
                    'addr:full': clean_street_name(shop['address']['street']),
                    'addr:city': shop['address']['town'],
                    'addr:postcode': shop['address']['postalCode'],
                    'phone': shop['address']['phone'],
                    'opening_hours': create_from_freetext('\n'.join(shop['openingHours']))
                }
            ))

        return FeatureCollection(features)
