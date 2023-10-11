import requests
from geojson import FeatureCollection, Feature, Point
from extractors import Extractor


class GroszekExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('https://groszek.com.pl/wp-content/themes/groszek/api/js/gps.json')
        data = response.json()

        features = []
        for shop in data['shops']:
            features.append(Feature(
                geometry=Point((shop['geolocation']['long'], shop['geolocation']['lat'])),
                properties={
                    'name': 'Groszek',
                    'brand': 'Groszek',
                    'shop': 'convenience',
                    'brand:wikidata': 'Q9280965',
                    'brand:wikipedia': 'pl:Groszek (sieć sklepów)',
                    'addr:streetname': shop['address']['street'],
                    'addr:housenumber': str(shop['address']['number']),
                    'addr:city': shop['address']['city'],
                    'addr:postcode': shop['address']['postalCode']
                }
            ))

        return FeatureCollection(features)
