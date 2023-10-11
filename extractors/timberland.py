import js2py
import requests

from geojson import FeatureCollection, Feature, Point
from bs4 import BeautifulSoup
from extractors import Extractor
from utils.opening_dates import create_from_freetext


def extract_json(content):
    soup = BeautifulSoup(content, 'html.parser')
    section = soup.select_one('.b-include')

    scripts = section.find_all('script', {'src': None})
    context = js2py.EvalJs()
    context.eval(scripts[0].text)
    return context.markers.to_list()


# todo opening hours
class TimberlandExtractor(Extractor):
    base_url = 'https://e-timberland.pl'
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0'

    def fetch_locations(self) -> FeatureCollection:
        response = requests.get(f'{self.base_url}/salony', headers={
            'User-Agent': self.user_agent
        })

        features = []
        entries = extract_json(response.content)
        for entry in entries:
            features.append(Feature(
                geometry=Point((float(entry['lng']), float(entry['lat']))),
                properties={
                    'name': 'Timberland',
                    'addr:full': entry['address'],
                    'addr:city': entry['city'],
                    'addr:postcode': entry['postcode'],
                    'phone': entry['phone'],
                    'email': entry['mail'],
                    'website': self.base_url + entry['url'],
                    'opening_hours': create_from_freetext(entry['hours'])
                }
            ))

        return FeatureCollection(features)
