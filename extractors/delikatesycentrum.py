from geojson import FeatureCollection, Feature, Point

from extractors import Extractor
from utils import extract_with_browser, extract_address_from_text, clean_street_name

from utils.opening_dates import OpeningHoursBuilder


class DelikatesyCentrumExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        data = extract_with_browser('https://www.delikatesy.pl/sklepy', """
            return window.__NEXT_DATA__.props.pageProps.shops;
        """)

        features = []
        for shop in data:
            if not shop['address']['lon'] or not shop['address']['lat']:
                continue

            builder = OpeningHoursBuilder()
            for opening_day in shop['opening_hours']:
                if opening_day['hours'] is None or '-' not in opening_day['hours']:
                    continue
                builder.add(opening_day['day'][:3], hour_range=opening_day['hours'])

            address_tags = extract_address_from_text(clean_street_name(shop['address']['street']))
            features.append(Feature(
                geometry=Point((float(shop['address']['lon']), float(shop['address']['lat']))),
                properties=address_tags | {
                    'ref': shop['shop_code'],
                    'name': 'Delikatesy Centrum',
                    'brand': 'Delikatesy Centrum',
                    'shop': 'supermarket',
                    'brand:wikidata': 'Q11693824',
                    'addr:full': shop['address']['street'],
                    'addr:city': shop['address']['city'],
                    'addr:postcode': shop['address']['post_code'],
                    'opening_hours': builder.build()
                }
            ))

        return FeatureCollection(features)
