import requests
from geojson import FeatureCollection, Feature, Point

from extractors import Extractor
from utils.opening_dates import OpeningHoursBuilder

CARREFOUR_TYPE_MAPPING = {
    'expressConvenience': {
        'name': 'Carrefour Express',
        'brand': 'Carrefour Express',
        'brand:wikidata': 'Q2940190',
        'shop': 'convenience'
    },
    'express': {
        'name': 'Carrefour Express',
        'brand': 'Carrefour Express',
        'brand:wikidata': 'Q2940190',
        'shop': 'convenience'
    },
    'market': {
        'name': 'Carrefour Market',
        'brand': 'Carrefour Market',
        'brand:wikidata': 'Q2689639',
        'shop': 'supermarket'
    },
    'supeco': {
        'name': 'Supeco',
        'brand:wikidata': 'Q110067293',
        'shop': 'supermarket'
    },
    'carrefour': {
        'name': 'Carrefour',
        'brand': 'Carrefour',
        'brand:wikidata': 'Q217599',
        'brand:wikipedia': 'fr:Carrefour (enseigne)',
        'shop': 'supermarket'
    },
    'globi': {
        'name': 'Globi',
        'shop': 'convenience'
    }
}


def get_carrefour_tags_for_type(shop):
    for key, value in CARREFOUR_TYPE_MAPPING.items():
        if key in shop['labels']:
            return value
    return None


class CarrefourExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        session = requests.Session()
        session.get('https://www.carrefour.pl/')
        response = session.get('https://www.carrefour.pl/web/pickup-locations?size=10000&shouldLabels=carrefour,market,express,expressConvenience,globi,supeco&mustLabels=locator')
        data = response.json()

        features = []
        for shop in data['content']:
            type_tags = get_carrefour_tags_for_type(shop)
            if not type_tags:
                print('skipped carrefour shop with unknown type')
                continue

            builder = OpeningHoursBuilder()
            if 'openTimes' in shop:
                for day_name, day_hours in shop['openTimes'].items():
                    builder.add(
                        day_name,
                        hour_from=f'{str(day_hours["openHour"]).zfill(2)}:{str(day_hours["openMinute"]).zfill(2)}',
                        hour_to=f'{str(day_hours["closeHour"]).zfill(2)}:{str(day_hours["closeMinute"]).zfill(2)}'
                    )

            features.append(Feature(
                geometry=Point((shop['lng'], shop['lat'])),
                properties=type_tags | {
                    'ref': shop['uuid'],
                    'addr:city': shop['city'],
                    'addr:street': shop['street'],
                    'addr:housenumber': shop['houseNumber'],
                    'addr:postcode': shop['zipCode'],
                    'phone': '+48 ' + shop['phoneNumber'] if 'phoneNumber' in shop else None,
                    'website': 'https://www.carrefour.pl/sklep/' + shop['slug'],
                    'opening_hours': builder.build()
                }
            ))

        return FeatureCollection(features)
