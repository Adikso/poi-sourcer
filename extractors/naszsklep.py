import requests
from geojson import FeatureCollection, Feature, Point
from extractors import Extractor
from utils import extract_address_from_text


class NaszSklepExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('https://www.nasz-sklep.pl/strefa-konsumenta/?paramAll=', headers={
            'X-Requested-With': 'XMLHttpRequest'
        })
        data = response.json()['shops']

        features = []
        for shop in data:
            address_tags = extract_address_from_text(shop['address']) if shop['address'] else dict()

            features.append(Feature(
                geometry=Point((float(shop['geo_lng']), float(shop['geo_lat']))),
                properties=address_tags | {
                    'ref': shop['id'],
                    'name': shop['name'],
                    'brand': 'Nasz Sklep',
                    'addr:full': shop['address'],
                    'addr:city': shop['town'],
                    'addr:postcode': shop['postcode']
                }
            ))

        return FeatureCollection(features)
