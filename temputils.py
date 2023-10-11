import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


def draw_pois(extractors):
    collection = []
    for extractor in extractors:
        # for i in range(3):
        try:
            print('extracting', extractor.__name__)
            locations = extractor().fetch_locations().get('features')
            collection += locations
            print(locations)
        except Exception as err:
            print('failed to extract', extractor.__name__, err)

    fig = plt.figure(figsize=(8, 8))
    m = Basemap(projection='lcc', resolution='i',
                width=0.7E6, height=0.7E6,
                lon_0=19.3, lat_0=52.2286378, )
    m.fillcontinents(color="#FFDDCC", lake_color='#DDEEFF')
    m.drawmapboundary(fill_color="#DDEEFF")
    m.drawcoastlines()
    m.drawcountries()

    print(len(collection))
    for entry in collection:
        x, y = m(entry['geometry']['coordinates'][0], entry['geometry']['coordinates'][1])
        plt.plot(x, y, 'ok', markersize=1)

    fig.show()
