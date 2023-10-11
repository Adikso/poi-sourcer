import requests
from geojson import Feature, Point, FeatureCollection

from extractors import Extractor
from utils import extract_address_from_text
from utils.opening_dates import OpeningHoursBuilder


class EmpikExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.post('https://www.empik.com/ajax/delivery-point/empik?query=', headers={
            'X-CSRF-TOKEN': '42adc778-4158-4646-8ca9-e97ce140da75',
            'Cookie': 'CSRF=42adc778-4158-4646-8ca9-e97ce140da75'
        })
        data = response.json()

        features = []
        for shop in data:
            hours = {
                'Mon': shop['mondayWorkingHours'],
                'Tue': shop['tuesdayWorkingHours'],
                'Wed': shop['wednesdayWorkingHours'],
                'Thu': shop['thursdayWorkingHours'],
                'Fri': shop['fridayWorkingHours'],
                'Sat': shop['saturdayWorkingHours'],
                'Sun': shop['sundayWorkingHours'],
            }

            builder = OpeningHoursBuilder()
            for key, value in hours.items():
                builder.add(key, hour_range=value)

            address_tags = extract_address_from_text(shop['address'])
            features.append(Feature(
                geometry=Point((float(shop['longitude']), float(shop['latitude']))),
                properties=address_tags | {
                    'name': 'Empik',
                    'brand': 'Empik',
                    'shop': 'books',
                    'brand:wikidata': 'Q3045978',
                    'brand:wikipedia': 'pl:Empik',
                    'addr:full': shop['address'],
                    'addr:city': shop['city'],
                    'addr:postcode': shop['postCode'],
                    'phone': shop['cellPhone'],
                    'email': shop['email'].strip(),
                    'opening_hours': builder.build()
                }
            ))
        return FeatureCollection(features)
