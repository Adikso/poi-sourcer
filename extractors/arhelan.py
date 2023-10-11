from geojson import FeatureCollection, Feature, Point
from extractors import Extractor
from utils import extract_with_browser
from utils.opening_dates import create_from_freetext


class ArhelanExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        data = extract_with_browser('https://arhelan.pl/nasze-sklepy/', """
            return locations;
        """)

        features = []
        for shop in data:
            features.append(Feature(
                geometry=Point((float(shop['lng']), float(shop['lat']))),
                properties={
                    'name': 'Arhelan',
                    'shop': 'supermarket',
                    'opening_hours': create_from_freetext(shop['godziny'])
                }
            ))

        return FeatureCollection(features)
