import requests
from geojson import FeatureCollection, Feature, Point
from geopy.geocoders import Nominatim

from extractors import Extractor
from utils import extract_address_from_text


class GlovoExtractor(Extractor):
    def _get_cuisine(self, restaurant_data):
        filters = [x['name'] for x in restaurant_data['filters']]
        if 'Kebab' in filters:
            return 'kebab'
        elif 'Burgery' in filters:
            return 'burger'
        elif 'Polskie' in filters:
            return 'polish'
        elif 'Sushi' in filters:
            return 'sushi'
        elif 'Pizza' in filters:
            return 'pizza'
        elif 'Azjatyckie' in filters:
            return 'asian'
        elif 'Indyjskie' in filters:
            return 'indian'
        return None

    def _is_fastfood(self, filters):
        return len(set(filters).intersection(['Kebab', 'Burgery'])) > 0

    def fetch_locations(self) -> FeatureCollection:
        headers = {
            "Glovo-API-Version": "14",
            "Glovo-App-Development-State": "Production",
            "Glovo-App-Platform": "web",
            "Glovo-App-Type": "customer",
            "Glovo-App-Version": "7",
            "Glovo-Device-Id": "1183568139",
            "Glovo-Language-Code": "pl"
        }
        features = []

        cities_res = requests.get('https://api.glovoapp.com/seo-content/locales/pl/countries/pl/cities', headers=headers)
        for city in cities_res.json()['cities']:
            if not city['slug']:
                continue
            city_details_res = requests.get(f'https://api.glovoapp.com/url-routing/resolve?urlPath=/pl/pl/{city["slug"]}/', headers=headers)
            city_details = city_details_res.json()
            city_code = city_details['resources']['city']['code']

            restaurants_res = requests.get('https://api.glovoapp.com/v3/feeds/categories/1?limit=10000&offset=0', headers=headers | {
                'Glovo-Location-City-Code': city_code
            })
            restaurants = restaurants_res.json()['elements']

            for restaurant in restaurants:
                try:
                    if restaurant['type'] != 'SINGLE' or restaurant['singleData']['type'] != 'STORE':
                        continue

                    restaurant_data = restaurant['singleData']['storeData']
                    store_data = restaurant_data['store']

                    filters = [x['name'] for x in restaurant_data['filters']]
                    keywords = store_data['suggestionKeywords']
                    strategies = [x['type'] for x in store_data['supportedStrategies']]
                    address_tags = extract_address_from_text(store_data['address'])

                    lat, lon = 0, 0
                    if store_data['location']:
                        lat = store_data['location']['latitude']
                        lon = store_data['location']['longitude']
                    else:
                        geolocator = Nominatim(user_agent="poimagic")
                        location = geolocator.geocode({
                            'street': f'{address_tags["addr:street"]} {address_tags["addr:housenumber"]}',
                            'city': address_tags['addr:city'],
                            'country': 'Poland',
                            'postalcode': address_tags['addr:postcode']
                        })
                        if location:
                            lat = location.latitude
                            lon = location.longitude

                    features.append(Feature(
                        geometry=Point((lon, lat)),
                        properties=address_tags | {
                            'name': store_data['name'],
                            'phone': store_data['phoneNumber'],
                            'amenity': 'fast_food' if self._is_fastfood(filters) else 'restaurant',
                            'addr:full': store_data['address'],
                            'cuisine': self._get_cuisine(restaurant_data),
                            'delivery': 'yes' if 'DELIVERY' in strategies else None,
                            'takeaway': 'yes' if 'PICKUP' in strategies else None,
                            'payment:cash': 'yes' if store_data['cashSupported'] else 'no',
                            'diet:vegetarian': 'yes' if 'wege' in keywords or 'vege' in keywords else None
                        }
                    ))
                except:
                    print('skipped')
            print('fetched', city['translatedName'])

        return FeatureCollection(features)
