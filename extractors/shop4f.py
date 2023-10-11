import requests
from geojson import FeatureCollection, Feature, Point
from extractors import Extractor


class Shop4FExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('https://4f.com.pl/graphql?query=query GetShops($store_id:Int){stationaryShops(store_id:$store_id){id name country_id city postcode address telephone email description latitude longitude type active personal_collection_enabled wms_id short_code __typename}}&operationName=GetShops&variables={"store_id":1}')
        data = response.json()

        features = []
        for shop in data['data']['stationaryShops']:
            features.append(Feature(
                geometry=Point((float(shop['longitude']), float(shop['latitude']))),
                properties={
                    'ref': shop['id'],
                    'name': '4F',
                    'brand': '4F',
                    'shop': 'sports',
                    'brand:wikidata': 'Q16525801',
                    'addr:full': shop['address'].replace('ul.', '').strip(),
                    'addr:city': shop['city'],
                    'addr:postcode': shop['postcode'],
                    'phone': shop['telephone'],
                    'email': shop['email']
                }
            ))

        return FeatureCollection(features)
