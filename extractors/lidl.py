import requests
from geojson import FeatureCollection, Feature, Point
from extractors import Extractor


# są szczegóły
from utils import clean_street_name
from utils.opening_dates import create_from_freetext


class LidlExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('https://stores.lidlplus.com/v2/PL')
        data = response.json()

        features = []
        for shop in data:
            hours = None
            try:
                hours = create_from_freetext(shop['schedule'])
            except:
                pass

            features.append(Feature(
                geometry=Point((shop['location']['longitude'], shop['location']['latitude'])),
                properties={
                    'ref': shop['storeKey'],
                    'name': 'Lidl',
                    'brand:wikidata': 'Q151954',
                    'brand:wikipedia': 'en:Lidl',
                    'shop': 'supermarket',
                    'addr:full': clean_street_name(shop['address']),
                    'addr:city': shop['locality'].capitalize(),
                    'addr:postcode': shop['postalCode'],
                    'opening_hours': hours,
                    'raw:opening_hours': shop['schedule'],
                }
            ))

        return FeatureCollection(features)
