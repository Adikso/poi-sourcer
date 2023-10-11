from geojson import FeatureCollection

WEEK_DAYS_SHORT_ARRAY = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
WEEK_DAYS_LONG_ARRAY = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
WEEK_DAYS_LONG_ARRAY_PL = ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek', 'Sobota', 'Niedziela']


def convert_to_short(name):
    name = name.strip()
    if name in WEEK_DAYS_LONG_ARRAY:
        return WEEK_DAYS_SHORT_ARRAY[WEEK_DAYS_LONG_ARRAY.index(name)]

    if name in WEEK_DAYS_LONG_ARRAY_PL:
        return WEEK_DAYS_SHORT_ARRAY[WEEK_DAYS_LONG_ARRAY_PL.index(name)]

    return None


class Extractor:
    def fetch_locations(self) -> FeatureCollection:
        pass

