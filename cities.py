import json

import requests
import re


pattern = re.compile(r'([0-9]{2}-[0-9]{3})')

with open('cities.json') as file:
    data = json.load(file)

cities = []
for region in data:
    for city in region['cities']:
        response = requests.get(f"https://nominatim.openstreetmap.org/search.php?q={city['lat']}%2C+{city['lon']}&format=jsonv2")
        match = pattern.findall(response.json()[0]['display_name'])
        if match:
            cities.append({
                'name': city['text_simple'],
                'lat': city['lat'],
                'lon': city['lon'],
                'postalCode': match[0],
            })

with open('cities_full.json', 'w') as file:
    json.dump(cities, file)
