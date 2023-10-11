import requests
from geojson import FeatureCollection, Feature, Point

from extractors import Extractor
from utils import extract_address_from_text


class EuroSklepExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('https://www.eurosklep.eu/nasze-sklepy?option=com_hotspots&view=jsonv4&task=gethotspots&hs-language=pl-PL&page=1&per_page=6000&cat=77&level=5&ne=58.45276,28.818701&sw=41.811239,10.405616&c=50.867508,19.612159&fs=0&offset=0&format=raw')
        data = response.json()

        features = []
        for shop in data['items']:
            address_tags = extract_address_from_text(shop['street']) if shop['street'].strip() else dict()

            features.append(Feature(
                geometry=Point((shop['lng'], shop['lat'])),
                properties=address_tags | {
                    'ref': shop['id'],
                    'name': 'Euro Sklep',
                    'shop': 'supermarket',
                    'addr:city': shop['city'],
                    'addr:postcode': shop['zip'],
                    'addr:full': shop['street'].strip()
                }
            ))

        return FeatureCollection(features)
