import requests
from geojson import FeatureCollection, Feature, Point
from extractors import Extractor
from utils import extract_address_from_text


class AuchanExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('https://api.auchan.com/corp/cms/v4/pl/template/stores?context=push-stores-list&lang=pl', headers={
            'X-Gravitee-Api-Key': 'f3fef77a-534a-4223-8907-47382f646efa'
        })
        data = response.json()

        features = []
        for shop in data:
            address_tags = extract_address_from_text(shop['address']['address'])
            features.append(Feature(
                geometry=Point((float(shop['address']['longitude']), float(shop['address']['latitude']))),
                properties=address_tags | {
                    'ref': shop['id'],
                    'name': 'Auchan',
                    'brand': 'Auchan',
                    'brand:wikidata': 'Q758603',
                    'brand:wikipedia': 'en:Auchan',
                    'shop': 'supermarket',
                    'addr:full': shop['address']['address'].split(',')[0],
                    'addr:city': shop['address']['city'],
                    'addr:postcode': shop['address']['postalCode']
                }
            ))

        return FeatureCollection(features)
