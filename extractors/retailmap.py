import js2py
import requests
from bs4 import BeautifulSoup
from geojson import FeatureCollection, Feature, Point

from extractors import Extractor
from utils.opening_dates import create_from_freetext


class RetailMapExtractor(Extractor):
    def fetch_locations(self) -> FeatureCollection:
        response = requests.get('https://www.propertynews.pl/retail-map/')
        soup = BeautifulSoup(response.content, 'html.parser')
        section = soup.select_one('body').find('script', {'src': None}).text

        context = js2py.EvalJs()
        context.eval("""
            var MAPA;
            MAPA = {
                'ustawDiv': function() { return MAPA; },
                'ustawZoom': function() { return MAPA; },
                'ustawDaneMarkerow': function() { return MAPA; },
                'pokazMape': function() { return MAPA; },
            }
        """)
        context.eval(section)
        entries = [{
            'name': x[0],
            'lat': x[1],
            'lon': x[2],
            'url': x[3]
        } for x in context.locations.to_list()]

        features = []
        for shop in entries:
            features.append(Feature(
                geometry=Point((float(shop['lon']), float(shop['lat']))),
                properties={
                    'name': shop['name'],
                    'website': shop['url']
                }
            ))

        return FeatureCollection(features)
