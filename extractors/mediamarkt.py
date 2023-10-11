# import requests
# from bs4 import BeautifulSoup
# from geojson import FeatureCollection, Feature, Point
# from extractors import Extractor
# from utils.opening_dates import create_from_freetext
#
#
# class MediaMarktExtractor(Extractor):
#     def fetch_locations(self) -> FeatureCollection:
#         response = requests.get('https://mediamarkt.pl/sklepy', {
#             "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0'
#         })
#         soup = BeautifulSoup(response.content, 'html.parser')
#         print(soup.find_all('script'))
#         script_with_data = list(filter(lambda x: 'marksArr' in x.text, soup.find_all('script')))
#         print(script_with_data)
#
#         features = []
#         # for shop in data:
#         #     features.append(Feature(
#         #         geometry=Point((float(shop['lon']), float(shop['lat']))),
#         #         properties={
#         #             'name': 'Wittchen',
#         #             'addr:full': shop['address'],
#         #             'addr:city': shop['city'],
#         #             'addr:postcode': shop['postcode'],
#         #             'phone': shop['phone'],
#         #             'opening_hours': create_from_freetext(shop['working_hours'])
#         #         }
#         #     ))
#
#         return FeatureCollection(features)
