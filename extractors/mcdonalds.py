import requests
from geojson import FeatureCollection, Feature, Point

from extractors import Extractor, WEEK_DAYS_SHORT_ARRAY


class McDonaldsExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('https://mcdonalds.pl/data/places')
        data = response.json()

        features = []
        for shop in data['places']:
            opening_hours = []
            for i, day in enumerate(shop['hours'].values()):
                opening_hours.append(f'{WEEK_DAYS_SHORT_ARRAY[i]} {day["from"]}-{day["to"]}')

            features.append(Feature(
                geometry=Point((float(shop['lng']), float(shop['lat']))),
                properties={
                    'name': 'McDonald\'s',
                    'brand': 'mcdonalds',
                    'amenity': 'fast_food',
                    'addr:full': shop['address'],
                    'addr:city': shop['city'],
                    'addr:postcode': shop['postCode'],
                    'phone': shop['phone'],
                    'opening_hours': ';'.join(opening_hours)
                }
            ))

        return FeatureCollection(features)
