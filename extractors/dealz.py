import json

import requests
from bs4 import BeautifulSoup
from geojson import FeatureCollection, Feature, Point

from extractors import Extractor
from utils import extract_address_from_text, clean_street_name
from utils.opening_dates import create_from_freetext


class DealzExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('https://www.dealz.pl/sklepy/')
        soup = BeautifulSoup(response.content, 'html.parser')
        shops_map = soup.select_one('div[shops-map-markers]')
        json_data = json.loads(shops_map.attrs['shops-map-markers'])

        features = []
        for shop in json_data:
            lng = float(shop['coordinates']['lng'])
            lat = float(shop['coordinates']['lat'])
            if lat == 0.0 and lng == 0.0:
                continue

            address_tags = dict()
            opening_hours_raw = None

            shop_box = soup.select_one(f'[shops-map-marker-html="{shop["shop_id"]}"]')
            if shop_box:
                address = clean_street_name(shop_box.select_one('.leaflet-popup__data').text.strip())
                opening_hours_raw = shop_box.select_one('.leaflet-popup__footer').text.strip()
                address_tags = extract_address_from_text(address)

            features.append(Feature(
                geometry=Point((lng, lat)),
                properties=address_tags | {
                    'name': 'Dealz',
                    'brand': 'Dealz',
                    'ref': str(shop['shop_id']),
                    'brand:wikidata': 'Q16942585',
                    'brand:wikipedia': 'en:Dealz',
                    'shop': 'variety_store',
                    'opening_hours': create_from_freetext(opening_hours_raw) if opening_hours_raw else None
                }
            ))

        return FeatureCollection(features)
