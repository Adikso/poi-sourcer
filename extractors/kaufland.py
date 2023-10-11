import requests
from geojson import FeatureCollection, Feature, Point
from extractors import Extractor
from utils import clean_street_name, extract_address_from_text
from utils.opening_dates import OpeningHoursBuilder


class KauflandExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('https://www.kaufland.pl/.klstorefinder.json')
        data = response.json()

        features = []
        for shop in data:
            builder = OpeningHoursBuilder()
            for entry in shop['wod']:
                parts = entry.split('|')
                builder.add(parts[0][:3], hour_from=parts[1], hour_to=parts[2])

            address_tags = extract_address_from_text(clean_street_name(shop['sn']))
            features.append(Feature(
                geometry=Point((float(shop['lng']), float(shop['lat']))),
                properties=address_tags | {
                    'name': 'Kaufland',
                    'brand': 'Kaufland',
                    'brand:wikidata': 'Q685967',
                    'brand:wikipedia': 'en:Kaufland',
                    'shop': 'supermarket',
                    'addr:full': shop['sn'],
                    'addr:city': shop['t'],
                    'addr:postcode': shop['pc'],
                    'phone': shop['p'],
                    'opening_hours': builder.build()
                }
            ))

        return FeatureCollection(features)
