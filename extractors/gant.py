import requests
from geojson import Feature, Point, FeatureCollection

from extractors import Extractor
from utils.opening_dates import OpeningHoursBuilder


class GantExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('https://pl.gant.com/stores/?format=json&country=67')
        data = response.json()

        features = []
        for shop in data['results']:
            if not shop['longitude'] or not shop['latitude']:
                continue

            builder = OpeningHoursBuilder()
            for i, day in enumerate(shop['store_hours']):
                if day[0] == '00:00:00' and day[1] == '00:00:00':
                    continue

                builder.add(i, hour_from=day[0], hour_to=day[1])

            features.append(Feature(
                geometry=Point((float(shop['longitude']), float(shop['latitude']))),
                properties={
                    'name': 'GANT',
                    'shop': 'clothes',
                    'brand:wikidata': 'Q1493667',
                    'brand:wikipedia': 'en:Gant (retailer)',
                    'addr:full': shop['address'],
                    'addr:city': shop['township']['city']['name'],
                    'addr:postcode': shop['township']['name'],
                    'phone': shop['phone_number'].replace('+ 48', '+48'),
                    'opening_hours': builder.build()
                }
            ))

        return FeatureCollection(features)
