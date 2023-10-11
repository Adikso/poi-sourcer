import requests
from geojson import FeatureCollection, Feature, Point

from extractors import Extractor


class PizzaHutExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        token_response = requests.post('https://kfcdostawa.pl/ordering-api/rest/v1/auth/get-token', json={
            'deviceUuid': 'FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF',
            'deviceUuidSource': 'FINGERPRINT',
            'source': 'WEB_PH'
        }, headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
            'Brand': 'PH'
        })
        token_data = token_response.json()

        response = requests.get('https://kfcdostawa.pl/ordering-api/rest/v2/restaurants/', headers={
            'Authorization': 'Bearer ' + token_data['token'],
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
            'Brand': 'PH'
        })
        data = response.json()

        features = []
        for shop in data['restaurants']:
            hours = [f'{x["openFrom"]}-{x["openTo"]}' for x in shop['openHours']]
            opening_hours = f'Mo-Su {",".join(hours)}'

            features.append(Feature(
                geometry=Point((float(shop['geoLng']), float(shop['geoLat']))),
                properties={
                    'name': 'Pizza Hut',
                    'brand:wikidata': 'Q191615',
                    'brand:wikipedia': 'en:Pizza Hut',
                    'addr:street': shop['addressStreet'],
                    'addr:housenumber': shop['addressStreetNo'] if 'addressStreetNo' in shop else None,
                    'addr:city': shop['addressCity'],
                    'addr:postcode': shop['addressPostalCode'],
                    'opening_hours': opening_hours
                }
            ))

        return FeatureCollection(features)