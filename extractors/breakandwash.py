from bs4 import BeautifulSoup
from geojson import FeatureCollection, Feature, Point
from extractors import Extractor
from utils import extract_with_browser, text_from_tag, extract_address_from_text


class BreakAndWashExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        data = extract_with_browser('https://breakandwash.pl/', """
            return window.locations;
        """)

        features = []
        for shop in data:
            soup = BeautifulSoup(shop['content'], 'html.parser')
            marker_content = text_from_tag(soup.select_one('.locations__markerContent'))
            address_tags = extract_address_from_text(marker_content)

            features.append(Feature(
                geometry=Point((float(shop['lng']), float(shop['lat']))),
                properties=address_tags | {
                    'name': 'Break & Wash',
                    'amenity': 'washing_machine',
                    'payment:coins': 'yes',
                    'payment:debit_cards': 'yes',
                    'payment:contactless': 'yes',
                    'website': 'https://breakandwash.pl/',
                }
            ))

        return FeatureCollection(features)
