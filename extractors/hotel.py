import requests
from geojson import FeatureCollection, Feature, Point
from extractors import Extractor


class HotelExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        features = []

        page = 0
        while True:
            response = requests.get(f'https://api.turystyka.gov.pl/registers/open/cwoh?size=10000&page={page}&processed=true')
            data = response.json()

            for shop in data['content']:
                features.append(Feature(
                    geometry=Point((float(shop['spatialLocation']['coordinates'][1]), float(shop['spatialLocation']['coordinates'][0]))),
                    properties={
                        'name': shop['name'],
                        'addr:full': shop['street'],
                        'addr:city': shop['city'],
                        'addr:postcode': shop['postalCode'],
                        'tourism': 'hotel',
                        'beds': shop['bedsNumber'],
                        'stars': shop['category'].count('*')
                    }
                ))

            if data['last']:
                break
            page += 1

        return FeatureCollection(features)
