import time

import requests
from geojson import FeatureCollection, Feature, Point
from extractors import Extractor
from utils import extract_address_from_text


class LeroyMerlinExtractor(Extractor):
    def _generate_hours_range(self, days_range, start, end):
        open = ((start - time.timezone * 1000) / 1000 / 60 / 60)
        close = ((end - time.timezone * 1000) / 1000 / 60 / 60)
        return f'{days_range} {str(int(open // 1)).zfill(2)}:{str(int((open % 1) * 60)).zfill(2)}-{str(int(close // 1)).zfill(2)}:{str(int((close % 1) * 60)).zfill(2)}'

    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('https://m.leroymerlin.pl/rest/v1/shops', headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0',
            'app-name': 'pl.leroymerlin.mobile',
            'app-platform': 'M_WWW',
            'app-version': '5.24.0',
            'app-version-name': 'BUGATTI',
        })
        data = response.json()

        features = []
        for shop in data:
            address_tags = extract_address_from_text(shop['street'])

            hours = [
                self._generate_hours_range('Mo-Fr', shop['openMondayToFriday'], shop['closeMondayToFriday']),
                self._generate_hours_range('Sa', shop['openSaturday'], shop['closeSaturday']),
                self._generate_hours_range('Su', shop['openSunday'], shop['closeSunday'])
            ]

            features.append(Feature(
                geometry=Point((shop['longitude'], shop['latitude'])),
                properties=address_tags | {
                    'ref': shop['shopCode'],
                    'name': 'Leroy Merlin',
                    'brand:wikidata': 'Q889624',
                    'shop': 'doityourself',
                    'addr:full': shop['street'],
                    'addr:city': shop['city'],
                    'addr:postcode': shop['postal'],
                    'phone': '+48 ' + shop['informationPointPhone'],
                    'website': 'https://www.leroymerlin.pl' + shop['wwwUrl'],
                    'opening_hours': ';'.join(hours)
                }
            ))

        return FeatureCollection(features)
