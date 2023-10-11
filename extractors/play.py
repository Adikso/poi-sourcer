import js2py
import requests
from geojson import FeatureCollection, Feature, Point
from extractors import Extractor


class PlayExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('https://media-play.pl/binaries/content/assets/play/portal/html/js/mapy/p4-map-data-salony.js')

        lines = response.text.splitlines()
        context = js2py.EvalJs()
        context.eval(lines[0])
        data = context.dataJson.to_list()

        features = []
        for shop in data:
            opening_hours = []
            if shop['mon-fri'] != 'nieczynne':
                opening_hours.append(f'Mo-Fr {shop["mon-fri"]}')
            if shop['sat'] != 'nieczynne':
                opening_hours.append(f'Sa {shop["sat"]}')
            if shop['sun'] != 'nieczynne':
                opening_hours.append(f'Su {shop["sun"]}')

            features.append(Feature(
                geometry=Point((float(shop['lng']), float(shop['lat']))),
                properties={
                    'ref': shop['sid'],
                    'brand:wikidata': 'Q7202998',
                    'name': 'Play',
                    'shop': 'mobile_phone',
                    'addr:full': shop['address'].replace('Ul.', '').strip(),
                    'addr:city': shop['city'],
                    'addr:postcode': shop['postal-code'],
                    'phone': shop['phone'],
                    'email': shop['email'],
                    'opening_hours': ';'.join(opening_hours)
                }
            ))

        return FeatureCollection(features)
