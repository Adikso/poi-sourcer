import requests
from geojson import FeatureCollection, Feature, Point
from extractors import Extractor
from utils import clean_street_name
from utils.opening_dates import convert_day_name


class TchiboExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('https://www.tchibo.pl/service/storefinder/api/storefinder/api/stores?page=0&size=100000&viewLng=18.985000&viewLat=51.685556&precision=606')
        data = response.json()

        features = []
        for shop in data['content']:
            if shop['addressDto']['country'] != 'PL' or shop['storeType'] not in ['Filiale', 'Percent']:
                continue

            opening_hours = []
            for key, value in shop['daysDto'].items():
                if value['morningOpening'] == 'null':
                    continue

                opening_hours.append(f'{convert_day_name(key)} {value["morningOpening"]}-{value["afternoonClosing"]}')

            features.append(Feature(
                geometry=Point((shop['locationGeographicDto']['lng'], shop['locationGeographicDto']['lat'])),
                properties={
                    'ref': shop['id'],
                    'brand:wikidata': 'Q564213',
                    'brand:wikipedia': 'de:Tchibo',
                    'name': 'Tchibo' if shop['storeType'] == 'Filiale' else 'Tchibo Outlet',
                    'addr:full': clean_street_name(shop['addressDto']['street']),
                    'addr:city': shop['addressDto']['city'],
                    'addr:postcode': shop['addressDto']['zip'],
                    'phone': shop['telephoneNumber'],
                    'opening_hours': ';'.join(opening_hours)
                }
            ))

        return FeatureCollection(features)
