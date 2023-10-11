import re

from bs4 import BeautifulSoup
from sortedcontainers import SortedDict

from extractors import WEEK_DAYS_SHORT_ARRAY

days_mapping = {
    'pon': 'Mo',
    'pn': 'Mo',
    'poniedzialek': 'Mo',
    'poniedziałek': 'Mo',
    'mon': 'Mo',
    'mo': 'Mo',
    'monday': 'Mo',
    'wto': 'Tu',
    'wt': 'Tu',
    'wtorek': 'Tu',
    'tu': 'Tu',
    'tue': 'Tu',
    'tuesday': 'Tu',
    'sro': 'We',
    'śro': 'We',
    'sroda': 'We',
    'środa': 'We',
    'wed': 'We',
    'we': 'We',
    'wednesday': 'We',
    'sr': 'We',
    'śr': 'We',
    'czw': 'Th',
    'cz': 'Th',
    'czwartek': 'Th',
    'thu': 'Th',
    'th': 'Th',
    'thursday': 'Th',
    'pia': 'Fr',
    'pią': 'Fr',
    'piątek': 'Fr',
    'piatek': 'Fr',
    'pt': 'Fr',
    'fri': 'Fr',
    'fr': 'Fr',
    'friday': 'Fr',
    'sob': 'Sa',
    'sb': 'Sa',
    'so': 'Sa',
    'sat': 'Sa',
    'sa': 'Sa',
    'saturday': 'Sa',
    'sobota': 'Sa',
    'nie': 'Su',
    'niedz': 'Su',
    'niedziela': 'Su',
    'ndz': 'Su',
    'nd': 'Su',
    'sun': 'Su',
    'su': 'Su',
    'sunday': 'Su',
}
tokenize_pattern = re.compile(r'((?:' + r'|'.join(days_mapping.keys()) + r')(?![a-zA-Z])|-|,|[0-9]{1,2}[:.][0-9]{1,2}|[a-zA-Z]{4,})')
hour_pattern = re.compile(r'[0-9]{1,2}[:.][0-9]{2}')


class SingleDay:
    def __init__(self, day):
        self.day = day

    def __str__(self):
        return days_mapping[self.day]


class MultipleDay:
    def __init__(self, days):
        self.days = days

    def __str__(self):
        return ','.join([days_mapping[x] for x in self.days])


class Range:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __str__(self):
        return f'{days_mapping[self.start]}-{days_mapping[self.end]}'


def create_from_freetext(text):
    soup = BeautifulSoup(text, "html.parser")
    if bool(soup.find()):
        return create_from_freetext(' '.join(soup.find_all(text=True)))

    tokenized_lines = [re.findall(tokenize_pattern, text.lower())]

    entry_dicts = []
    for line in tokenized_lines:
        days = None
        day_start = None
        operation = None
        buffer = []
        hours = []
        for i, token in enumerate(line):
            # there is more days
            if len(hours) == 2 and token in days_mapping.keys():
                tokenized_lines.append(line[i:])
                break

            if token == '-':
                operation = token
            if token == ',':
                operation = token
                if not buffer:
                    buffer = [day_start]

            if re.match(hour_pattern, token):
                hours.append(token.rjust(5, '0').replace('.', ':'))
                if day_start:
                    if not operation:
                        days = SingleDay(day_start)
                        day_start = None
                if operation == ',' and buffer:
                    days = MultipleDay(buffer)
                    buffer = []

            if token in days_mapping.keys():
                if not day_start:
                    day_start = token
                elif day_start and operation == '-':
                    days = Range(day_start, token)
                    day_start = None
                    operation = None
                elif operation == ',':
                    buffer.append(token)

        if not days:
            continue

        entry_dicts.append(f'{days} {"-".join(hours)}')

    return '; '.join(entry_dicts)


def convert_day_name(name):
    return days_mapping[name.lower()]


class OpeningHoursBuilder:
    def __init__(self):
        self.entries = SortedDict()

    def add(self, day, hour_from='', hour_to='', hour_range=''):
        if isinstance(day, str):
            day = WEEK_DAYS_SHORT_ARRAY.index(days_mapping[day.lower()])

        if hour_to == '00:00':
            hour_to = '24:00'

        if hour_range:
            parts = hour_range.split('-')
            self.entries[day] = f'{parts[0].zfill(5)}-{parts[1].zfill(5)}'
        else:
            hour_from = ':'.join(hour_from.split(':')[:2])
            hour_to = ':'.join(hour_to.split(':')[:2])
            self.entries[day] = f'{hour_from.zfill(5)}-{hour_to.zfill(5)}'

    def build(self):
        opening_hours = []

        range_start = None
        last_value = None
        for day, value in self.entries.items():
            if value != last_value:
                if last_value:
                    if range_start != day - 1:
                        opening_hours.append(f'{WEEK_DAYS_SHORT_ARRAY[range_start]}-{WEEK_DAYS_SHORT_ARRAY[day - 1]} {last_value}')
                    else:
                        opening_hours.append(f'{WEEK_DAYS_SHORT_ARRAY[range_start]} {last_value}')

                last_value = value
                range_start = day

        if last_value:
            last_day = list(self.entries.keys())[-1]
            if range_start != last_day:
                opening_hours.append(f'{WEEK_DAYS_SHORT_ARRAY[range_start]}-{WEEK_DAYS_SHORT_ARRAY[last_day]} {last_value}')
            else:
                opening_hours.append(f'{WEEK_DAYS_SHORT_ARRAY[range_start]} {last_value}')

        return ';'.join(opening_hours)
