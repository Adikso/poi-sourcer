import requests
from bs4 import BeautifulSoup
from geojson import FeatureCollection, Feature, Point
from extractors import Extractor
from utils import text_from_tag, extract_js_var_from_html, extract_address_from_text


class ChortenExtractor(Extractor):
    @staticmethod
    def _fetch_data():
        response = requests.get('https://chorten.com.pl/sklepy/mapa')
        return extract_js_var_from_html(response.content, 'data', simple=True)

    def fetch_locations(self) -> FeatureCollection:
        data = self._fetch_data()

        features = []
        for shop in data['sklepy']:
            if not shop['lat']:
                continue

            soup = BeautifulSoup(shop['ttip'], 'html.parser')
            address_tag = soup.select_one('.address')
            address_text = text_from_tag(address_tag).strip()
            address_tags = extract_address_from_text(address_text)

            features.append(Feature(
                geometry=Point((shop['lng'], shop['lat'])),
                properties=address_tags | {
                    'ref': shop['id'],
                    'name': shop['title'],
                    'brand': 'Chorten',
                    'brand:wikidata': 'Q48843988',
                    'shop': 'convenience'
                }
            ))

        return FeatureCollection(features)
