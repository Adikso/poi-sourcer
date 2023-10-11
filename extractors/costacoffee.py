import datetime

import requests
from geojson import FeatureCollection, Feature, Point

from extractors import Extractor
from utils import extract_address_from_text
from utils.opening_dates import OpeningHoursBuilder


class CostaCoffeeExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('https://api.costacoffee.pl/api/storelocator/list', headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0'
        })
        data = response.json()

        features = []
        for shop in data:
            builder = OpeningHoursBuilder()
            add_opening_hours = True

            for opening_entry in shop['openingHours']:
                if opening_entry['isException']:
                    add_opening_hours = False
                    break

                if not opening_entry["hourFrom"] or not opening_entry["hourTo"]:
                    continue

                weekday = datetime.datetime.strptime(f"{opening_entry['day']}.{datetime.datetime.today().year}", '%d.%m.%Y').weekday()
                builder.add(weekday, hour_from=opening_entry["hourFrom"], hour_to=opening_entry["hourTo"])

            address_tags = extract_address_from_text(shop['address']) if shop['address'] else dict()

            features.append(Feature(
                geometry=Point((float(shop['gpsX']), float(shop['gpsY']))),
                properties=address_tags | {
                    'name': 'Costa Coffee',
                    'brand': 'Costa Coffee',
                    'brand:wikidata': 'Q608845',
                    'brand:wikipedia': 'en:Costa Coffee',
                    'cuisine': 'coffee_shop',
                    'amenity': 'cafe',
                    'addr:full': shop['address'],
                    'addr:city': shop['city'],
                    'addr:postcode': shop['postCode'],
                    'opening_hours': builder.build() if add_opening_hours else None,
                    'delivery': 'yes' if shop['deliveryAvailable'] else 'no'
                }
            ))

        return FeatureCollection(features)
