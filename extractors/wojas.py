import csv
import io

import requests
from geojson import FeatureCollection, Feature, Point

from extractors import Extractor

DAYS_MAPPING = {
    'pn': 'Mo',
    'pon': 'Mo',
    'wt': 'Tu',
    'śr': 'We',
    'czw': 'Th',
    'cz': 'Th',
    'pt': 'Fr',
    'sb': 'Sa',
    'nd': 'Su'
}


class WojasExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('https://wojas.pl/storelocator.csv', headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0'
        })
        response.encoding = "utf-8"
        reader = csv.DictReader(io.StringIO(response.text), delimiter=',')

        features = []
        for entry in reader:
            if entry['Fcilty_typ_2'] != 'http://www.wojas.pl':
                continue

            fields = parse_human_fields(entry['Hrs_of_bus'])
            features.append(Feature(
                geometry=Point((float(entry['Xcoord']), float(entry['Ycoord']))),
                properties={
                    'name': 'Wojas',
                    'addr:full': entry['Street_add'],
                    'addr:city': entry['Shp_num_an'],
                    'addr:postcode': entry['Postcode'],
                    'phone': fields['phone'],
                    'email': fields['email'],
                    'opening_hours': fields['opening_hours']
                }
            ))

        return FeatureCollection(features)


def parse_human_fields(text):
    fields = {
        'phone': None,
        'email': None,
        'opening_hours': None
    }

    human_data = text \
        .replace(' – ', '-') \
        .replace(' - ', '-') \
        .replace(' -', '-') \
        .replace('- ', '-') \
        .replace(', ', ',') \
        .split('<br>')
    human_fields = dict(([y.strip(' :.') for y in x.lower().strip().split(' ', maxsplit=1)] for x in human_data))

    opening_hours = []
    for key, value in human_fields.items():
        if key == 'tel':
            fields['phone'] = value
            continue
        if key == 'e-mail':
            fields['email'] = value
            continue

        if ' ' in value:
            opening_hours = None
            break

        key_range = ''
        if '-' in key:
            days_range = key.split('-')
            from_day = DAYS_MAPPING[days_range[0]]
            to_day = DAYS_MAPPING[days_range[1]]

            key_range = f'{from_day}-{to_day}'
        elif ',' in key:
            key_range = ','.join([DAYS_MAPPING[x] for x in key.split(',')])
        elif key in DAYS_MAPPING.keys():
            key_range = DAYS_MAPPING[key]

        opening_hours.append(f'{key_range} {value}')

    fields['opening_hours'] = '; '.join(opening_hours) if opening_hours else None
    return fields
