from typing import List

import requests

# from extractors import Extractor, POI, Address, Opening
#
#
# class OchnikExtractor(Extractor):
#     def fetch_locations(self) -> List[POI]:
#         login_response = requests.post('https://ochnik.com/api/frontend/pl/tokens/guest', data={
#             'guestId': 'Ab155a67-629a-4dc0-b72a-bbfb49376031'
#         }, headers={
#             'Accept-Version': '4'
#         })
#         login_data = login_response.json()
#         access_token = login_data['accessToken']['token']
#
#         pois = []
#         page = 1
#         while True:
#             response = requests.get(f'https://ochnik.com/api/frontend/pl/pos/outpost?page={page}', headers={
#                 'Authorization': f'Bearer {access_token}',
#                 'Accept-Version': '3'
#             })
#             data = response.json()
#
#             for shop in data['items']:
#                 address = Address()
#                 address.raw = shop['address']
#                 address.city = shop['address']['cityName']
#                 address.post_code = shop['address']['postalCode']
#                 address.house_number = shop['address']['buildingNumber']
#                 address.street = shop['address']['streetName']
#
#                 hours = {}
#                 for day in shop['openingHours']['days']:
#                     hours[day['name'].capitalize()] = Opening(
#                         opening=day['timeRanges'][0]['from'],
#                         closing=day['timeRanges'][0]['to']
#                     )
#
#                 poi = POI(
#                     name=shop['name'],
#                     lat=str(shop['coordinates']['latitude']),
#                     lon=str(shop['coordinates']['longitude']),
#                     address=address,
#                     hours=hours
#                 )
#
#                 if shop['contactData']:
#                     if shop['contactData']['phoneNumbers']:
#                         poi.phone = shop['contactData']['phoneNumbers'][0]['value']
#                     if shop['contactData']['emails']:
#                         poi.email = shop['contactData']['emails'][0]['value']
#
#                 pois.append(poi)
#
#             if data['pagination']['lastPage'] == data['pagination']['currentPage']:
#                 break
#
#             page = data['pagination']['currentPage'] + 1
#
#         return pois