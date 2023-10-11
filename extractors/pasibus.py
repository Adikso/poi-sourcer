import requests
from bs4 import BeautifulSoup
from geojson import FeatureCollection, Feature, Point

from extractors import Extractor, convert_to_short


class PasibusExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('https://pasibus.pl/Umbraco/Api/Coordinates/GetAllCoordinates?currentPageId=1082', headers={
            'Content-Type': 'application/json'
        })
        data = response.json()

        features = []
        for shop in data:
            soup = BeautifulSoup(shop['openingHours'], 'html.parser')
            days = soup.find_all('p')
            opening_hours = []
            for day in days:
                week_day = day.select_one('.week-day').text
                hours = day.select_one('.open-hours').text
                opening_hours.append(f'{convert_to_short(week_day)} {hours}')

            features.append(Feature(
                geometry=Point((float(shop['position']['longitude']), float(shop['position']['latitude']))),
                properties={
                    'name': 'Pasibus',
                    'amenity': 'fast_food',
                    'addr:full': shop['street'],
                    'addr:city': shop['city'],
                    'addr:postcode': shop['postcode'],
                    'phone': shop['phone'],
                    'website': 'https://pasibus.pl' + shop['url'],
                    'opening_hours': '; '.join(opening_hours)
                }
            ))

        return FeatureCollection(features)
