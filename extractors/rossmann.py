from typing import List

import requests
from geojson import Feature, Point, FeatureCollection

from extractors import Extractor, WEEK_DAYS_LONG_ARRAY
from utils import flip_dict


class RossmannExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('https://www.rossmann.pl/shops/api/Shops')
        data = response.json()

        features = []
        for shop in data['data']:
            hours = {}
            opening_hours = []

            for day_name in WEEK_DAYS_LONG_ARRAY:
                if f'{day_name.lower()}OpenFrom' in shop['openHours']:
                    hours[day_name] = f"{shop['openHours'][f'{day_name.lower()}OpenFrom']}-{shop['openHours'][f'{day_name.lower()}OpenTo']}"

            for key, value in flip_dict(hours).items():
                opening_hours.append(f'{",".join(value)} {key}')

            features.append(Feature(
                geometry=Point((float(shop['shopLocation']['longitude']), float(shop['shopLocation']['latitude']))),
                properties={
                    'name': 'Rossmann',
                    'brand:wikidata': 'Q316004',
                    'brand:wikipedia': 'pl:Rossmann',
                    # 'name': shop['shopNumber'],
                    'addr:full': shop['address']['street'],
                    'addr:city': shop['address']['city'],
                    'addr:postcode': shop['address']['postCode'],
                    'opening_hours': '; '.join(opening_hours)
                }
            ))

        return FeatureCollection(features)
