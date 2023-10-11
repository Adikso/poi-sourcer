import json

import requests
from geojson import FeatureCollection, Feature, Point
from extractors import Extractor


# todo
from utils import clean_street_name


class AdidasExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('https://placesws.adidas-group.com/API/search?brand=adidas&geoengine=google&method=get&category=store&latlng=51.71655064990832%2C17.40198689785025&page=1&pagesize=5000&fields=name%2Cstreet1%2Cstreet2%2Caddressline%2Cbuildingname%2Cpostal_code%2Ccity%2Cstate%2Cstore_o+wner%2Ccountry%2Cstoretype%2Clongitude_google%2Clatitude_google%2Cstore_owner%2Cstate%2Cperformance%2Cbrand_store%2Cfactory_outlet%2Coriginals%2Cneo_label%2Cy3%2Cslvr%2Cchildren%2Cwoman%2Cfootwear%2Cfootball%2Cbasketball%2Coutdoor%2Cporsche_design%2Cmiadidas%2Cmiteam%2Cstella_mccartney%2Ceyewear%2Cmicoach%2Copening_ceremony%2Coperational_status%2Cfrom_date%2Cto_date%2Cdont_show_country&format=json&storetype=ownretail')
        data = response.content.replace(b'\n', b'\\n').replace(b'\r', b'\\r').replace(b'\\2', b'\\\\2')
        data = json.loads(data, strict=False)

        features = []
        for shop in data['wsResponse']['result']:
            if shop['country'] != 'PL':
                continue

            features.append(Feature(
                geometry=Point((float(shop['longitude_google']), float(shop['latitude_google']))),
                properties={
                    'ref': shop['id'],
                    'name': 'Adidas',
                    'brand:wikidata': 'Q3895',
                    'brand:wikipedia': 'en:Adidas',
                    'shop': 'sports',
                    'addr:full': clean_street_name(shop['street1']),
                    'addr:city': shop['city'],
                    'addr:postcode': shop['postal_code']
                }
            ))

        return FeatureCollection(features)
