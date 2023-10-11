import js2py
import requests
from bs4 import BeautifulSoup
from geojson import FeatureCollection, Feature, Point
from extractors import Extractor
from utils import extract_address_from_text
from utils.opening_dates import create_from_freetext


class GromulskiExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('https://www.piekarniagromulski.pl/gdzie-kupic/')
        soup = BeautifulSoup(response.text, 'html.parser')

        context = js2py.EvalJs()
        markers = response.text.split('var markers = ')[1].split(';')[0]
        context.eval(f'var markers = {markers};')
        data = context['markers']

        features = []
        for shop in data:
            map_info = soup.select_one(f'#nr{shop[0]}')
            address = map_info.select_one('#addres').text

            open_wd = map_info.select_one('#open_wd').text
            open_we = map_info.select_one('#open_we').text

            address_tags = extract_address_from_text(address)
            features.append(Feature(
                geometry=Point((float(shop[2]), float(shop[1]))),
                properties=address_tags | {
                    'ref': shop[0],
                    'name': 'Gromulski',
                    'brand': 'Gromulski',
                    'brand:wikidata': 'Q113308317',
                    'shop': 'bakery',
                    'opening_hours': create_from_freetext(open_wd + '\n' + open_we)
                }
            ))

        return FeatureCollection(features)
