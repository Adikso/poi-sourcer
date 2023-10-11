import requests
from geojson import FeatureCollection, Feature, Point
from extractors import Extractor


# są godziny otwarcia
from utils import clean_street_name


class LevisExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.post('https://www.levi.com/nextgen-webhooks/?operationName=storeDirectory&locale=PL-pl_PL', json={
            'operationName': 'storeDirectory',
            'query': 'query storeDirectory($countryIsoCode: String!) {  storeDirectory(countryIsoCode: $countryIsoCode) {    storeFinderData {      addLine1      addLine2      city      country      departments      distance      hrsOfOperation {        daysShort        hours        isOpen      }      latitude      longitude      mapUrl      ors      phone      postcode      state      storeId      storeName      storeType      todaysHrsOfOperation {        daysShort        hours        isOpen      }      uom    }  }}',
            'variables': {
                'countryIsoCode': 'PL'
            }
        }, headers={
            'X-BRAND': 'levi',
            'X-LOCALE': 'pl_PL',
            'X-COUNTRY': 'PL',
            'X-OPERATIONNAME': 'storeDirectory'
        })
        data = response.json()

        features = []
        for shop in data['data']['storeDirectory']['storeFinderData']:
            features.append(Feature(
                geometry=Point((shop['longitude'], shop['latitude'])),
                properties={
                    'name': 'Levi\'s',
                    'addr:full': clean_street_name(shop['addLine1']),
                    'addr:city': shop['city'],
                    'addr:postcode': shop['postcode'],
                    'phone': shop['phone'],
                }
            ))

        return FeatureCollection(features)
