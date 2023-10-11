import requests
from geojson import FeatureCollection, Feature, Point
from extractors import Extractor
from utils.opening_dates import create_from_freetext


class WittchenExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('https://www.wittchen.com/api/v1/delivery-points/pl-PL')
        data = response.json()

        features = []
        for shop in data:
            features.append(Feature(
                geometry=Point((float(shop['lon']), float(shop['lat']))),
                properties={
                    'name': 'Wittchen',
                    'addr:full': shop['address'],
                    'addr:city': shop['city'],
                    'addr:postcode': shop['postcode'],
                    'phone': shop['phone'],
                    'opening_hours': create_from_freetext(shop['working_hours'])
                }
            ))

        return FeatureCollection(features)
