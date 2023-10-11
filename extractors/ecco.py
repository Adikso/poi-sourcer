import requests
from geojson import Feature, Point, FeatureCollection

from extractors import Extractor
# wrong


class ECCOExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('https://pl.ecco.com/api/store/search?latitudeMin=43.33154750332266&longitudeMin=9.191751646875002&latitudeMax=59.34885909496308&longitudeMax=29.077005553125')
        data = response.json()

        features = []
        for shop in data:
            features.append(Feature(
                geometry=Point((float(shop['lon']), float(shop['lat']))),
                properties={
                    'name': 'Ecco',
                    'addr:full': shop['address'],
                    'addr:city': shop['city'],
                    'addr:postcode': shop['postcode'],
                    'phone': shop['phone']
                }
            ))
        return FeatureCollection(features)
