import requests
from geojson import FeatureCollection, Feature, Point
from extractors import Extractor


# todo opening hours
class ObiExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('https://www.obi.pl/storeLocatorRest/v1/stores/getAllByCountry/pl/pl?fields=name,address,phone,services,hours,storeNumber,path,email', headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0'
        })
        data = response.json()

        features = []
        for shop in data['stores']:
            features.append(Feature(
                geometry=Point((shop['address']['lon'], shop['address']['lat'])),
                properties={
                    'ref': shop['storeId'],
                    'name': 'OBI',
                    'brand:wikidata': 'Q300518',
                    'brand:wikipedia': 'de:Obi (Baumarkt)',
                    'shop': 'doityourself',
                    'addr:full': shop['address']['street'],
                    'addr:city': shop['address']['city'],
                    'addr:postcode': shop['address']['zip'],
                    'phone': shop['phone']
                }
            ))

        return FeatureCollection(features)
