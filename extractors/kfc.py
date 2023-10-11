import requests
from geojson import FeatureCollection, Feature, Point

from extractors import Extractor
from utils.opening_dates import OpeningHoursBuilder


class KFCExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        token_response = requests.post('https://kfcdostawa.pl/ordering-api/rest/v1/auth/get-token', json={
            'deviceUuid': 'FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF',
            'deviceUuidSource': 'FINGERPRINT',
            'source': 'WEB_KFC'
        }, headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0'
        })
        token_data = token_response.json()

        response = requests.get('https://kfcdostawa.pl/ordering-api/rest/v2/restaurants/', headers={
            'Authorization': 'Bearer ' + token_data['token'],
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0'
        })
        data = response.json()

        features = []
        for shop in data['restaurants']:
            builder = OpeningHoursBuilder()
            if shop['openHours']:
                for day_name in ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']:
                    builder.add(
                        day_name,
                        hour_from=shop['openHours'][0]['openFrom'],
                        hour_to=shop['openHours'][0]['openTo']
                    )

            features.append(Feature(
                geometry=Point((float(shop['geoLng']), float(shop['geoLat']))),
                properties={
                    'name': 'KFC',
                    'brand': 'KFC',
                    'amenity': 'fast_food',
                    'brand:wikidata': 'Q524757',
                    'brand:wikipedia': 'en:KFC',
                    'addr:street': shop['addressStreet'],
                    'addr:housenumber': shop['addressStreetNo'] if 'addressStreetNo' in shop else None,
                    'addr:city': shop['addressCity'],
                    'addr:postcode': shop['addressPostalCode'],
                    'opening_hours': builder.build()
                }
            ))

        return FeatureCollection(features)
