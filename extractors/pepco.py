import json
import re

import requests
from bs4 import BeautifulSoup
from geojson import FeatureCollection, Feature, Point

from extractors import Extractor, WEEK_DAYS_SHORT_ARRAY

address_pattern = re.compile(r'(?P<street>.*)(?P<postal>[0-9]{2}-[0-9]{3}) (?P<city>.*)')
hours_pattern = re.compile(r'(?P<from>[0-9]{2}:[0-9]{2}) - (?P<to>[0-9]{2}:[0-9]{2})')


class PepcoExtractor(Extractor):
    BASE_URL = 'https://pepco.pl/sklepy/'
    AJAX_URL = 'https://pepco.pl/wp-admin/admin-ajax.php'

    def fetch_locations(self) -> FeatureCollection:
        response = requests.get(self.BASE_URL)
        soup = BeautifulSoup(response.content, 'html.parser')
        shops_map = soup.select_one('div[shops-map-markers]')
        json_data = json.loads(shops_map.attrs['shops-map-markers'])

        page = 0
        buffer = ""
        for i in range(1000):  # Max value todo
            page_res = requests.post(self.AJAX_URL, data={
                'action': 'get_more_shops',
                'page': str(page),
            })

            data = page_res.json()
            buffer += data['shops']
            page = data['page']

            if data['last_page']:
                break

        soup = BeautifulSoup(buffer, 'html.parser')
        html_entries = soup.find_all('div', {'shops-map-marker-anchor': True})

        entries = {}
        for entry in html_entries:
            address_text = soup.select_one('.col-24').find_all('p')[0].text
            address_parts = address_pattern.match(address_text).groupdict()

            hours_days_dom = soup.select_one('.find-shop-box__open-table').find_all('td')
            open_hours = []
            for i, hours_entry in enumerate(hours_days_dom):
                match = hours_pattern.match(hours_entry.text)
                if match:
                    groups = match.groupdict()
                    open_hours.append(f'{WEEK_DAYS_SHORT_ARRAY[i]} {groups["from"]}-{groups["to"]}')

            entries[entry.attrs['shops-map-marker-anchor']] = {
                'addr:full': address_parts['street'].strip(' ,.'),
                'addr:city': address_parts['city'],
                'addr:postcode': address_parts['postal'],
                'opening_hours': ';'.join(open_hours)
            }

        features = []
        for shop in json_data:
            ref = str(shop['shop_id'])
            lng = float(shop['coordinates']['lng'])
            lat = float(shop['coordinates']['lat'])
            if lat == 0.0 and lng == 0.0:
                continue

            if ref not in entries:
                continue

            features.append(Feature(
                geometry=Point((lng, lat)),
                properties={
                    'name': 'Pepco',
                    'ref': str(shop['shop_id']),
                    'brand:wikidata': 'Q11815580',
                    'brand:wikipedia': 'pl:Pepco'
                } | entries[ref]
            ))

        return FeatureCollection(features)
