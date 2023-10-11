import json
import requests
from geojson import FeatureCollection, Feature, Point

from extractors import Extractor
from utils import extract_with_browser
from utils.opening_dates import create_from_freetext


class EObuwieExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        data = extract_with_browser('https://www.eobuwie.com.pl/sklepy', """
            return gmapPoints;
        """)

        # response = requests.get('https://www.eobuwie.com.pl/sklepy')
        #
        # start_tag = b"var gmapPoints = JSON.parse( '"
        # end_tag = b"');"
        #
        # start_index = response.content.index(start_tag) + len(start_tag)
        # end_index = response.content.index(end_tag, start_index)
        # json_data = response.content[start_index:end_index]
        # data = json.loads(json_data)

        features = []
        for shop in data['points']:
            features.append(Feature(
                geometry=Point((float(shop['long']), float(shop['lat']))),
                properties={
                    'name': 'Eobuwie',
                    'shop': 'shoes',
                    'addr:full': shop['adres']['street'],
                    'opening_hours': create_from_freetext('\n'.join(list(shop['open'].values())))
                }
            ))

        return FeatureCollection(features)
