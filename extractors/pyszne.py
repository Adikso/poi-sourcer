import json
import multiprocessing

import requests
from geojson import FeatureCollection, Feature, Point

from extractors import Extractor


def fetch(city):
    response = requests.get(f'https://cw-api.takeaway.com/api/v32/restaurants?postalCode={city}&limit=0&isAccurate=true', headers={
        'X-Country-Code': 'pl'
    })
    data = response.json()

    city_features = []
    for shop in data['restaurants'].values():
        if not shop['location']['lng'] or not shop['location']['lat']:
            continue

        city_features.append(Feature(
            geometry=Point((float(shop['location']['lng']), float(shop['location']['lat']))),
            properties={
                'ref': shop['id'],
                'name': shop['brand']['name'],
                'addr:full': shop['location']['streetAddress'],
                'addr:city': shop['location']['city']
            }
        ))
    # print(len(city_features))
    return city_features


class PyszneExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        with open('cities_full.json') as file:
            cities = json.load(file)

        pool = multiprocessing.Pool(6)
        res = pool.map(fetch, [x["postalCode"] for x in cities])
        complete = []
        for a in res:
            complete += a

        tracker = set()
        clean = []
        for x in complete:
            if x.properties['ref'] in tracker:
                continue
            tracker.add(x.properties['ref'])
            clean.append(x)

        return FeatureCollection(clean)
