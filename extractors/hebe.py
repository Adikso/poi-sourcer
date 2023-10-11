import requests
from bs4 import BeautifulSoup
from geojson import FeatureCollection, Feature, Point

from extractors import Extractor
from utils import extract_address_from_text
from utils.opening_dates import create_from_freetext


class HebeExtractor(Extractor):
    BASE_URL = 'https://www.hebe.pl'

    def fetch_locations(self) -> FeatureCollection:
        response = requests.get(f'{self.BASE_URL}/sklepy')
        soup = BeautifulSoup(response.content, 'html.parser')

        features = []
        shops = soup.select('.storelist__item')
        for shop in shops:
            street = shop.select_one('.store-popup__address').text
            city_postcode = shop.select_one('.store-popup__city').text
            addr_full = f'{street}, {city_postcode}'
            address_tags = extract_address_from_text(addr_full)

            opening_date_div = shop.select_one('.store-comming-soon__date')
            opening_hours_div = shop.select_one('.store-hours')

            features.append(Feature(
                geometry=Point((float(shop['data-lng']), float(shop['data-lat']))),
                properties=address_tags | {
                    'ref': shop['data-id'],
                    'name': 'Hebe',
                    'brand': 'Hebe',
                    'brand:wikidata': 'Q113093841',
                    'shop': 'chemist',
                    'operator': 'Jeronimo Martins Drogerie i Farmacja Sp. z o.o.',
                    'addr:full': addr_full,
                    'website': self.BASE_URL + shop.select_one('.js-choose-store')['href'],
                    'opening_hours': create_from_freetext(opening_hours_div.text) if opening_hours_div else None,
                    'opening_date': opening_date_div.text.strip() if opening_date_div else None
                }
            ))

        return FeatureCollection(features)
