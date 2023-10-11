import requests
from bs4 import BeautifulSoup
from geojson import FeatureCollection, Feature, Point

from extractors import Extractor
from utils import extract_address_from_text, user_agent
from utils.opening_dates import create_from_freetext


class PoloMarketExtractor(Extractor):
    BASE_URL = 'https://www.polomarket.pl'

    def fetch_locations(self) -> FeatureCollection:
        response = requests.get(f'{self.BASE_URL}/pl/nasze-sklepy.html', headers={
            'User-Agent': user_agent()
        })
        soup = BeautifulSoup(response.content, 'html.parser')
        regions_links = ['/'.join([self.BASE_URL, x["href"]]) for x in soup.find_all('area')]

        features = []
        for region_link in regions_links:
            response = requests.get(region_link, headers={
                'User-Agent': user_agent()
            })

            soup = BeautifulSoup(response.content, 'html.parser')
            shops = soup.select('.region')
            for shop in shops:
                city = shop.find('span', string='Miasto:').nextSibling.text.strip()
                street = shop.find('span', string='Ulica:').nextSibling.text.strip()
                opening_hours_raw = shop.find('span', string='Godziny otwarcia:').nextSibling.text
                navigate_url = shop.find('a', string='Dojazd')
                address_tags = extract_address_from_text(street)

                features.append(Feature(
                    geometry=Point((float(navigate_url['data-lng']), float(navigate_url['data-lat']))),
                    properties=address_tags | {
                        'name': 'POLOMarket',
                        'brand': 'POLOMarket',
                        'brand:wikidata': 'Q11821937',
                        'shop': 'supermarket',
                        'addr:full': street,
                        'addr:city': city,
                        'opening_hours': create_from_freetext(opening_hours_raw)
                    }
                ))

        return FeatureCollection(features)
