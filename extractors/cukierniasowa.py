import requests
from collections import OrderedDict
from geojson import FeatureCollection, Feature, Point
from phpserialize import loads

from extractors import Extractor
from utils import extract_address_from_text, clean_street_name
from utils.opening_dates import OpeningHoursBuilder


class CukierniaSowaExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('https://www.cukierniasowa.pl/home/shops?str=&reg=&type=0&geo=&alias=&typee=&count=')

        features = []
        for shop in response.json():
            if shop['location_country'] != 'Polska':
                continue

            opening_hours_raw = list(loads(shop['location_hours'].encode('utf-8'), array_hook=OrderedDict).values())
            builder = OpeningHoursBuilder()

            for i, entry in enumerate(opening_hours_raw[:7]):
                if entry[b'disabled'] == b'1':
                    continue
                builder.add(
                    i,
                    hour_from=f'{entry[b"open"][b"hour"].decode()}:{entry[b"open"][b"minute"].decode()}',
                    hour_to=f'{entry[b"close"][b"hour"].decode()}:{entry[b"close"][b"minute"].decode()}',
                )

            address_tags = extract_address_from_text(clean_street_name(shop['location_street']))
            features.append(Feature(
                geometry=Point((float(shop['location_lng']), float(shop['location_lat']))),
                properties=address_tags | {
                    'name': 'Cukiernia Sowa',
                    'brand': 'Cukiernia Sowa',
                    'addr:city': shop['location_city'],
                    'addr:full': shop['location_street'],
                    'phone': '+48 ' + shop['location_phone'],
                    'email': shop['location_email'],
                    'website': 'https://www.cukierniasowa.pl/cukiernie/' + shop['location_url'],
                    'opening_hours': builder.build()
                }
            ))

        return FeatureCollection(features)
