import requests
from geojson import FeatureCollection, Feature, Point
from extractors import Extractor
from utils import extract_address_from_text, clean_street_name
from utils.opening_dates import convert_day_name, OpeningHoursBuilder


class HMExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('https://api.storelocator.hmgroup.tech/v2/brand/hm/stores/locale/pl_pl/country/PL?_type=json&campaigns=true&departments=true&openinghours=true&maxnumberofstores=1000')
        data = response.json()

        features = []
        for shop in data['stores']:
            builder = OpeningHoursBuilder()
            for day in shop['openingHours']:
                day_name = convert_day_name(day['name'].replace('.', ''))
                builder.add(day_name, hour_from=day["opens"], hour_to=day["closes"])

            clothes = []
            for concept in shop['departmentsWithConcepts']:
                if concept['name'] == 'DAMSKI':
                    clothes.append('women')
                elif concept['name'] == 'MĘSKI':
                    clothes.append('men')
                elif concept['name'] == 'DZIECIĘCY':
                    clothes.append('children')

            address_tags = dict()
            address_raw = clean_street_name(shop['address']['streetName2'])
            if address_raw:
                address_tags = extract_address_from_text(clean_street_name(shop['address']['streetName2']))

            features.append(Feature(
                geometry=Point((shop['longitude'], shop['latitude'])),
                properties=address_tags | {
                    'name': 'H&M',
                    'brand:wikidata': 'Q188326',
                    'brand:wikipedia': 'en:H&M',
                    'shop': 'clothes',
                    'clothes': ';'.join(clothes) if clothes else None,
                    'addr:full': shop['address']['streetName2'],
                    'addr:city': shop['city'],
                    'addr:postcode': shop['address']['postCode'],
                    'phone': shop['phone'],
                    'opening_hours': builder.build()
                }
            ))

        return FeatureCollection(features)
