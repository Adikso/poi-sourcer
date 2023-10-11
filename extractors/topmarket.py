import requests
from geojson import FeatureCollection, Feature, Point
from extractors import Extractor


class TopMarketExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('https://www.topmarkety.pl/wp-admin/admin-ajax.php?action=asl_load_stores&load_all=1&layout=1', verify=False)
        data = response.json()

        features = []
        for shop in data:
            lat = float(shop['lat'].replace(',', '.'))
            lng = float(shop['lng'].replace(',', '.'))

            features.append(Feature(
                geometry=Point((lng, lat)),
                properties={
                    'ref': shop['id'],
                    'name': 'TopMarket',
                    'addr:full': shop['street'],
                    'addr:city': shop['city'],
                    'addr:postcode': shop['postal_code'],
                    'phone': shop['phone']
                }
            ))

        return FeatureCollection(features)
