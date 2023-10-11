import requests
from geojson import FeatureCollection, Feature, Point
from extractors import Extractor
from utils import clean_street_name, extract_address_from_text
from utils.opening_dates import OpeningHoursBuilder


class SparExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.post('https://spar.pl/wp-admin/admin-ajax.php', data={
            'action': 'shopsincity',
            'lat': '51.7592485',
            'lng': '19.4559833',
            'distance': '500000'
        })
        data = response.json()

        features = []
        for shop in data['locations']:
            if not shop['lng'] or not shop['lat']:
                continue

            address_tags = extract_address_from_text(shop['adres'])
            hours_builder = OpeningHoursBuilder()

            days_names = ['poniedzialek', 'wtorek', 'sroda', 'czwartek', 'piatek', 'sobota', 'niedziela']
            for i, day_name in enumerate(days_names):
                if day_name in shop and shop[day_name] != 'nieczynne':
                    hours_builder.add(i, hour_range=shop[day_name])

            features.append(Feature(
                geometry=Point((float(shop['lng'].replace(',', '')), float(shop['lat'].replace(',', '')))),
                properties=address_tags | {
                    'ref': shop['id'],
                    'name': shop['format'].capitalize(),
                    'addr:full': clean_street_name(shop['adres']),
                    'addr:city': shop['miasto'],
                    'addr:postcode': shop['kod'],
                    'opening_hours': hours_builder.build(),
                    'website': shop['permalink']
                }
            ))

        return FeatureCollection(features)
