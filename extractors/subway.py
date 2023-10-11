import json
import re
import requests
from geojson import FeatureCollection, Feature, Point
from extractors import Extractor

pins_pattern = re.compile(r'cspm_new_pin_object\(map_id, (.*)\);')


class SubwayExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('https://mysubway.pl/mapa')
        all_jsons = pins_pattern.findall(response.text)
        pins = [json.loads(x) for x in all_jsons]

        features = []
        for shop in pins:
            features.append(Feature(
                geometry=Point((float(shop['coordinates']['lng']), float(shop['coordinates']['lat']))),
                properties={
                    'name': 'Subway',
                    'website': shop['link'] if 'link' in shop else None
                }
            ))

        return FeatureCollection(features)
