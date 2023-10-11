import js2py
import requests
from bs4 import BeautifulSoup
from geojson import FeatureCollection, Feature, Point
from extractors import Extractor
from utils import extract_address_from_text


class CastoramaExtractor(Extractor):
    @staticmethod
    def _fetch_data():
        response = requests.get('https://www.castorama.pl/informacje/sklepy')
        soup = BeautifulSoup(response.content, 'html.parser')
        locations_script = soup.find(lambda tag: tag.name == 'script' and 'EVENT_MARKETS_INSIDE_PHTML_LOADED' in tag.text)

        context = js2py.EvalJs()
        context.eval('var bold = { trigger: function(name, value) { result = value; } }')
        context.eval(locations_script.text)
        return context.result

    def fetch_locations(self) -> FeatureCollection:
        data = self._fetch_data()

        features = []
        for shop in data['marketsAll']:
            address_tags = extract_address_from_text(shop['street'])

            opening_hours = []
            if 'pnpt' in shop:
                opening_hours.append(f'Mo-Fr {shop["pnpt"]}')
            if 'sb' in shop:
                opening_hours.append(f'Sa {shop["sb"]}')
            if 'nd' in shop:
                opening_hours.append(f'Su {shop["nd"]}')

            features.append(Feature(
                geometry=Point((float(shop['longitude']), float(shop['latitude']))),
                properties=address_tags | {
                    'ref': shop['id'],
                    'name': 'Castorama',
                    'brand:wikidata': 'Q966971',
                    'brand:wikipedia': 'en:Castorama',
                    'shop': 'doityourself',
                    'addr:full': shop['street'],
                    'addr:city': shop['city'],
                    'addr:postcode': shop['code'],
                    'phone': shop['phone'],
                    'website': shop['url_rewrite'],
                    'fax': shop['fax'],
                    'opening_hours': ';'.join(opening_hours)
                }
            ))

        return FeatureCollection(features)
