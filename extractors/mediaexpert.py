import requests
from geojson import FeatureCollection, Feature, Point
from extractors import Extractor


# cloudflare got me
class MediaExpertExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('https://sklepy.mediaexpert.pl/data/getshops', headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0'
        })
        data = response.json()

        features = []
        for shop in data:
            opening_hours = []
            for key, value in shop.items():
                if not key.startswith('open_') or value == 'Nieczynne':
                    continue
                parts = key.split('_')
                opening_hours.append(f'{parts[0].capitalize()} {value.replace(" ", "")}')

            features.append(Feature(
                geometry=Point((float(shop['lng']), float(shop['lat']))),
                properties={
                    'ref': shop['code'],
                    'name': 'Media Expert',
                    'addr:full': shop['address'],
                    'addr:city': shop['city_name'],
                    'addr:postcode': shop['zip'],
                    'phone': shop['phone'],
                    'website': 'https://sklepy.mediaexpert.pl/' + shop['url'],
                    'opening_hours': ';'.join(opening_hours)
                }
            ))

        return FeatureCollection(features)
