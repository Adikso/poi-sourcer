import re

import requests
from geojson import FeatureCollection, Feature, Point
from extractors import Extractor
from utils.opening_dates import create_from_freetext


token_pattern = re.compile(r"<script>window\.CSRF_TOKEN = '([a-z0-9-]{36})';<\/script>")


class SmykExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        session = requests.Session()
        response = session.get('https://www.smyk.com/storelocator')
        csrf_match = token_pattern.findall(response.text, re.MULTILINE)
        csrf_token = csrf_match[0]

        response = session.post('https://www.smyk.com/gateway/api/portal/delivery-channels/stores/locator', json={
            'facilities': [],
            'page': 1,
            'pageSize': 1000,
            'searchPhrase': ''
        }, headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0',
            'X-CSRF-TOKEN': csrf_token
        })
        data = response.json()

        features = []
        for shop in data['content']:
            opening_hours = [f'{entry["days"]} {entry["hours"]}' for entry in shop['openingHours']]

            if not shop['geoLongitude'] or not shop['geoLatitude']:
                continue

            features.append(Feature(
                geometry=Point((float(shop['geoLongitude']), float(shop['geoLatitude']))),
                properties={
                    'ref': shop['code'],
                    'name': 'Smyk',
                    'addr:street': shop['street'],
                    'addr:housenumber': shop['streetNumber'],
                    'addr:city': shop['city'],
                    'addr:postcode': shop['zipCode'],
                    'phone': shop['phone'],
                    'opening_hours': create_from_freetext('\n'.join(opening_hours))
                }
            ))

        return FeatureCollection(features)
