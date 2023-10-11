import re

import requests
from geojson import FeatureCollection, Feature, Point
from extractors import Extractor


hours_pattern = re.compile(r'([0-9]{1,}:[0-9]{2})-([0-9]{1,}:[0-9]{2})')


class IntermarcheExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('https://intermarche.pl/wp-content/themes/intermarche/json/markers.json')
        data = response.json()

        features = []
        for shop in data:
            opening_hours = []
            if hours_pattern.match(shop['open_mon_fri']):
                opening_hours.append(f'Mo-Fr {shop["open_mon_fri"].zfill(11)}')
            if hours_pattern.match(shop['open_sat']):
                opening_hours.append(f'Sa {shop["open_sat"].zfill(11)}')
            if hours_pattern.match(shop['open_sun']):
                opening_hours.append(f'Su {shop["open_sun"].zfill(11)}')

            features.append(Feature(
                geometry=Point((float(shop['lng']), float(shop['lat']))),
                properties={
                    'ref': shop['number'],
                    'name': 'Intermarche',
                    'shop': 'supermarket',
                    'addr:full': shop['street'].replace('ul.', '').strip(),
                    'addr:city': shop['city'],
                    'addr:postcode': shop['zip'],
                    'phone': shop['phone'] if shop['phone'] else None,
                    'email': shop['email'] if shop['email'] else None,
                    'opening_hours': ';'.join(opening_hours)
                }
            ))

        return FeatureCollection(features)
