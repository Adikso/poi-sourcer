from bs4 import BeautifulSoup
from geojson import FeatureCollection, Feature, Point

from extractors import Extractor
from utils import extract_with_browser, extract_address_from_text


class TKMaxxExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        data = extract_with_browser('https://www.tkmaxx.pl/znajdz-sklep', """
            return Drupal.settings.gmap.auto1map.markers;
        """)

        features = []
        for marker in data:
            soup = BeautifulSoup(marker['text'], 'html.parser')
            address_field = next(x for x in soup.select('.field-content') if 'ul.' in x.text)
            city_field = address_field.next
            address_tags = extract_address_from_text(address_field.text)

            features.append(Feature(
                geometry=Point((float(marker['longitude']), float(marker['latitude']))),
                properties=address_tags | {
                    'name': 'TK Maxx',
                    'brand': 'TK Maxx',
                    'shop': 'department_store',
                    'brand:wikidata': 'Q23823668',
                    'brand:wikipedia': 'en:TK Maxx',
                    'addr:full': address_field
                }
            ))
