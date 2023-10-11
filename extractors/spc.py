from geojson import FeatureCollection, Feature, Point
from extractors import Extractor
from utils import extract_with_browser


class SPCExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        data = extract_with_browser('https://spc.pl/nasze-sklepy/', """
            return Object.entries(map2).filter(e => e[0].startsWith('jQuery'))[0][1]['wpgmp_maps']['places'].map(place => ({
               id: place.id,
               address: place.address,
               city: place.location.city,
               postcode: place.location.postal_code,
               location: {
                  lat: place.location.lat,
                  lng: place.location.lng
               }
            }));
        """)

        features = []
        for shop in data:
            features.append(Feature(
                geometry=Point((float(shop['location']['lng']), float(shop['location']['lat']))),
                properties={
                    'ref': shop['id'],
                    'name': 'SPC',
                    'shop': 'bakery',
                    'addr:full': shop['address'],
                    'addr:city': shop['location']['city'] if 'city' in shop['location'] else None,
                    'addr:postcode': shop['location']['postal_code'] if 'postal_code' in shop['location'] else None
                }
            ))

        return FeatureCollection(features)
