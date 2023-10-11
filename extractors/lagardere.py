import requests
from geojson import FeatureCollection, Feature, Point
from extractors import Extractor
from utils import extract_address_from_text, clean_street_name


class LagardereExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('http://sklepy.lagardere-tr.pl/data/shop_locations.json?origLat=52.30093434229163&origLng=20.948078536328143')
        data = response.json()

        features = []
        for shop in data:
            address_tags = extract_address_from_text(clean_street_name(shop['street']))

            base = address_tags | {
                'ref': shop['psd'],
                'addr:full': shop['street'],
                'addr:city': shop['city'],
                'addr:postcode': shop['postal'],
                'phone': shop['phone']
            }

            if shop['logoid'] == 'INM':
                features.append(Feature(
                    geometry=Point((float(shop['lng']), float(shop['lat']))),
                    properties=base | {
                        'name': 'Inmedio',
                        'brand:wikidata': 'Q108599411',
                        'shop': 'newsagent',
                    }
                ))
            elif shop['logoid'] == 'SOC':
                features.append(Feature(
                    geometry=Point((float(shop['lng']), float(shop['lat']))),
                    properties=base | {
                        'name': 'SO! COFFEE',
                        'amenity': 'cafe',
                    }
                ))
            elif shop['logoid'] == '1-M':
                features.append(Feature(
                    geometry=Point((float(shop['lng']), float(shop['lat']))),
                    properties=base | {
                        'name': '1-Minute',
                        'shop': 'convenience',
                    }
                ))
            elif shop['logoid'] == 'REL':
                features.append(Feature(
                    geometry=Point((float(shop['lng']), float(shop['lat']))),
                    properties=base | {
                        'name': 'Relay',
                        'shop': 'newsagent',
                    }
                ))
            elif shop['logoid'] == 'IQOS':
                features.append(Feature(
                    geometry=Point((float(shop['lng']), float(shop['lat']))),
                    properties=base | {
                        'name': 'IQOS',
                        'shop': 'e-cigarette',
                    }
                ))
            elif shop['logoid'] == 'INMC':
                features.append(Feature(
                    geometry=Point((float(shop['lng']), float(shop['lat']))),
                    properties=base | {
                        'name': 'Inmedio Cafe',
                        'amenity': 'cafe',
                    }
                ))
            elif shop['logoid'] == 'TRENDY':
                features.append(Feature(
                    geometry=Point((float(shop['lng']), float(shop['lat']))),
                    properties=base | {
                        'name': 'Inmedio Trendy',
                        'shop': 'convenience',
                    }
                ))
            elif shop['logoid'] == 'HELLO':
                features.append(Feature(
                    geometry=Point((float(shop['lng']), float(shop['lat']))),
                    properties=base | {
                        'name': 'HELLO',
                        'shop': 'bakery',
                    }
                ))
            elif shop['logoid'] == 'HUB':
                features.append(Feature(
                    geometry=Point((float(shop['lng']), float(shop['lat']))),
                    properties=base | {
                        'name': 'Hubiz',
                        'shop': 'newsagent',
                    }
                ))
            elif shop['logoid'] == 'PREMIUM':
                features.append(Feature(
                    geometry=Point((float(shop['lng']), float(shop['lat']))),
                    properties=base | {
                        'name': 'Premium Food',
                        'shop': 'deli',
                    }
                ))
            elif shop['logoid'] == 'DISC':
                features.append(Feature(
                    geometry=Point((float(shop['lng']), float(shop['lat']))),
                    properties=base | {
                        'name': 'Discover',
                        'shop': 'gift',
                    }
                ))
            elif shop['logoid'] == 'VIRGIN':
                features.append(Feature(
                    geometry=Point((float(shop['lng']), float(shop['lat']))),
                    properties=base | {
                        'name': 'Virgin',
                        'shop': 'books',
                    }
                ))
            elif shop['logoid'] == 'CHIEFS':
                features.append(Feature(
                    geometry=Point((float(shop['lng']), float(shop['lat']))),
                    properties=base | {
                        'name': 'Chiefs Bistro',
                        'amenity': 'restaurant',
                    }
                ))
            elif shop['logoid'] == 'PAUL':
                features.append(Feature(
                    geometry=Point((float(shop['lng']), float(shop['lat']))),
                    properties=base | {
                        'name': 'Paul',
                        'amenity': 'restaurant',
                    }
                ))
            elif shop['logoid'] == 'FS':
                features.append(Feature(
                    geometry=Point((float(shop['lng']), float(shop['lat']))),
                    properties=base | {
                        'name': 'Furore!',
                        'amenity': 'ice_cream',
                    }
                ))
            elif shop['logoid'] == 'FLAME':
                features.append(Feature(
                    geometry=Point((float(shop['lng']), float(shop['lat']))),
                    properties=base | {
                        'name': 'ILLY',
                        'amenity': 'cafe',
                    }
                ))

        return FeatureCollection(features)
