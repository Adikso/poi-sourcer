import requests
from geojson import FeatureCollection, Feature, Point
from extractors import Extractor, WEEK_DAYS_SHORT_ARRAY


class TMobileExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('https://www.t-mobile.pl/c/_bffapi/sdr-shops/v1/shops')
        data = response.json()

        features = []
        for shop in data:
            opening_hours = []
            for i, day in enumerate(['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']):
                if shop["hours"][day + "_from"] == '-':
                    continue
                opening_hours.append(f'{WEEK_DAYS_SHORT_ARRAY[i]} {shop["hours"][day + "_from"]}-{shop["hours"][day + "_to"]}')

            features.append(Feature(
                geometry=Point((shop['coordinates']['x'], shop['coordinates']['y'])),
                properties={
                    'brand:wikidata': 'Q327634',
                    'name': 'T-Mobile',
                    'shop': 'mobile_phone',
                    'addr:street': shop['address']['street'],
                    'addr:housenumber': shop['address']['street_no'],
                    'addr:city': shop['address']['city'],
                    'addr:postcode': shop['address']['post_code'],
                    'phone': shop['contact']['phone'],
                    'email': shop['contact']['email'],
                    'opening_hours': ';'.join(opening_hours)
                }
            ))

        return FeatureCollection(features)
