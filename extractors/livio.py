import js2py
import requests
from geojson import FeatureCollection, Feature, Point
from extractors import Extractor
from utils import remove_html


class LivioExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('https://liviosklepy.pl/sites/all/modules/custom/invMaps/area/markers-17-pl.js')

        context = js2py.EvalJs()
        context.eval('var Drupal = {};')
        context.eval(response.text)
        data = context.Drupal.invMaps

        features = []
        for shop in data['markers']:
            features.append(Feature(
                geometry=Point((float(shop['longitude']), float(shop['latitude']))),
                properties={
                    'name': shop['nazwa'],
                    'brand': 'Livio',
                    'addr:full': remove_html(shop['marker']['field_inv_maps_street']),
                    'addr:postcode': remove_html(shop['marker']['field_inv_maps_zip_code']),
                    'addr:city': shop['city']
                }
            ))

        return FeatureCollection(features)
