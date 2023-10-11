import requests
from geojson import FeatureCollection, Feature, Point
from extractors import Extractor


class OdidoExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('https://www.sklepy-odido.pl/api/shops?page=1&itemsPerPage=10000')
        data = response.json()

        features = []
        for shop in data['data']:
            if 'lat' not in shop:
                continue

            features.append(Feature(
                geometry=Point((float(shop['lon']), float(shop['lat']))),
                properties={
                    'name': 'Odido',
                    'shop': 'convenience',
                    'addr:street': shop['Ulica'],
                    'addr:housenumber': shop['Numer budynku'],
                    'addr:city': shop['city'],
                    'addr:postcode': shop['postcode']
                }
            ))

        return FeatureCollection(features)
