from itertools import islice
import requests
from geojson import Feature, Point, FeatureCollection

from extractors import Extractor


def chunk(arr_range, arr_size):
    arr_range = iter(arr_range)
    return iter(lambda: tuple(islice(arr_range, arr_size)), ())


class ZabkaExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        points_response = requests.get('https://www.zabka.pl/ajax/shop-clusters.json')
        points_data = points_response.json()

        all_ids = []
        for entry in points_data:
            all_ids.append(entry['id'])

        features = []
        for chunk_part in chunk(all_ids, 1000):
            response = requests.post('https://apkykk0pza-dsn.algolia.net/1/indexes/*/objects', headers={
                'X-Algolia-API-Key': '71ca67cda813cec86431992e5e67ede2',
                'X-Algolia-Application-Id': 'APKYKK0PZA'
            }, json={
                "requests": [
                    {
                        "indexName": "prod_locator_prod_zabka",
                        "objectID": id
                    }
                    for id in chunk_part
                ]
            })

            data = response.json()
            for entry in data['results']:
                features.append(Feature(
                    geometry=Point((float(entry['_geoloc']['lng']), float(entry['_geoloc']['lat']))),
                    properties={
                        'name': 'Żabka',
                        'brand': 'Żabka',
                        'brand:wikidata': 'Q2589061',
                        'shop': 'convenience',
                        'addr:full': entry['address'],
                        'addr:city': entry['city'],
                        'addr:postcode': entry['postcode'],
                    }
                ))

        return FeatureCollection(features)
