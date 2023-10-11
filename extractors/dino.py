import re

import requests
from bs4 import BeautifulSoup
from geojson import FeatureCollection, Feature, Point

from extractors import Extractor
from utils import extract_address_from_text, clean_street_name, capitalize_names
from utils.opening_dates import create_from_freetext

postal_pattern = re.compile(r'(([0-9]+) ?- ?([0-9]+))')


class DinoExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('https://marketdino.pl/wp-json/wpgmza/v1/features/?filter={"map_id":"36","mashupIDs":[],"customFields":[]}')
        data = response.json()

        features = []
        for shop in data['markers']:
            soup = BeautifulSoup(shop['description'], 'html.parser')
            all_rows = [x.text for x in soup.find_all('p')]

            if not all_rows:
                continue

            address_tags = dict()
            raw_address = clean_street_name(all_rows[1]).strip()
            if raw_address:
                address_tags = extract_address_from_text(raw_address)

            postal_code = postal_pattern.search(' '.join(all_rows)).group().replace(' ', '')

            features.append(Feature(
                geometry=Point((float(shop['lng']), float(shop['lat']))),
                properties=address_tags | {
                    'name': 'Dino',
                    'brand': 'Dino',
                    'brand:wikidata': 'Q11694239',
                    'brand:wikipedia': 'pl:Dino Polska',
                    'shop': 'supermarket',
                    'ref': str(shop['id']),
                    'addr:full': all_rows[1],
                    'addr:city': capitalize_names(all_rows[0]),
                    'addr:postcode': postal_code,
                    'opening_hours': create_from_freetext('\n'.join(all_rows[3:]))
                }
            ))

        return FeatureCollection(features)
