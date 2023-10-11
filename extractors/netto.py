import requests
from geojson import FeatureCollection, Feature, Point
from extractors import Extractor


class NettoExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('https://www.netto.pl/umbraco/api/StoresData/StoresV2')
        data = response.json()

        features = []
        for shop in data:
            features.append(Feature(
                geometry=Point((float(shop['coordinates'][0]), float(shop['coordinates'][1]))),
                properties={
                    'name': 'Netto',
                    'brand': 'Netto',
                    'shop': 'supermarket',
                    'brand:wikidata': 'Q552652',
                    'brand:wikipedia': 'da:Netto (supermarkedskæde)',
                    'addr:full': shop['address']['street'],
                    'addr:city': shop['address']['city'],
                    'addr:postcode': shop['address']['zip'],
                    'website': 'https://www.netto.pl/' + shop['url']
                }
            ))

        return FeatureCollection(features)
