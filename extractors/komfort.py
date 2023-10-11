from geojson import FeatureCollection, Feature, Point

from extractors import Extractor
from utils import extract_with_browser
from utils.opening_dates import OpeningHoursBuilder


class KomfortExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        result = extract_with_browser('https://komfort.pl/sklepy', """
            return window.__INITIAL_STATE__.marketplace.shops.shops;
        """)

        features = []
        for entry in result:
            builder = OpeningHoursBuilder()
            for hour in entry['hours']:
                builder.add(hour["day"], hour_from=hour["start_hour"], hour_to=hour["end_hour"])

            features.append(Feature(
                geometry=Point((float(entry['geo_lon']), float(entry['geo_lat']))),
                properties={
                    'ref': entry['identifier'],
                    'name': 'Komfort',
                    'shop': 'furniture',
                    'addr:city': entry['city'],
                    'addr:street': entry['street_name'],
                    'addr:housenumber': entry['street_number'],
                    'addr:postcode': entry['postcode'],
                    'phone': entry['phone'],
                    'email': entry['email'],
                    'opening_hours': builder.build()
                }
            ))

        return FeatureCollection(features)
