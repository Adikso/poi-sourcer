import asyncio
import json

import js2py
import reverse_geocode
from bs4 import BeautifulSoup
from esprima import esprima
from pyppeteer import launch

from deepparse.parser import AddressParser

address_parser = AddressParser(model_type="bpemb", device=0)


class DummyAddressParser:
    def __call__(self, *args, **kwargs):
        return self

    def to_dict(self):
        return dict()


# address_parser = DummyAddressParser()


def flip_dict(d):
    flipped = {}

    for key, value in d.items():
        if value not in flipped:
            flipped[value] = [key]
        else:
            flipped[value].append(key)

    return flipped


def is_in_poland(coords):
    return reverse_geocode.search([coords])[0]['country_code'] == 'PL'


def clean_street_name(name):
    return name.replace('Ul.', '').replace('ul.', '').strip()


def remove_html(content):
    soup = BeautifulSoup(content, 'html.parser')
    return soup.text


def texts_from_html(content):
    soup = BeautifulSoup(content, 'html.parser')
    return soup.find_all(text=True)


def text_from_tag(tag, delimiter=' '):
    return delimiter.join(tag.find_all(text=True))


def extract_js_var_from_html(body, var_name, simple=False):
    soup = BeautifulSoup(body, 'html.parser')
    all_scripts = soup.find_all('script')

    for script in all_scripts:
        if var_name not in script.text:
            continue
        var_value = extract_var_from_js(script.text, var_name, simple=simple)
        if var_value is not None:
            return var_value


def extract_var_from_js(content, var_name, simple=False):
    if var_name not in content:
        return

    var_content = ''

    def callback(node, meta):
        nonlocal var_content
        if node.type != 'VariableDeclarator':
            return

        if node.id.name != var_name:
            return

        var_content = content[node.init.range[0]:node.init.range[1]]

    esprima.parseScript(content, {"range": True}, callback)

    if not simple:
        context = js2py.EvalJs()
        context.eval(var_content)

        return context[var_name]
    else:
        return json.loads(var_content)


def extract_with_browser(url, code=None, intercept_response=None):
    result = None

    async def main():
        nonlocal result
        browser = await launch({'headless': True, 'executablePath': '/usr/bin/chromium'})
        page = await browser.newPage()

        if intercept_response:
            page.on('response', intercept_response)

        # await page.goto(url, {'waitUntil': 'networkidle0'})
        await page.goto(url, {'waitUntil': 'networkidle0'})

        if code:
            result = await page.evaluate(f'''() => {{
                {code}
            }}''')

        await browser.close()

    asyncio.get_event_loop().run_until_complete(main())
    return result


def extract_address_from_text(content):
    address = address_parser(clean_street_name(content)).to_dict()
    tags = dict()

    if 'StreetName' in address and address['StreetName']:
        tags['addr:street'] = capitalize_names(address['StreetName'])

    if 'StreetNumber' in address and address['StreetNumber']:
        tags['addr:housenumber'] = address['StreetNumber']

    if 'Municipality' in address and address['Municipality']:
        tags['addr:city'] = capitalize_names(address['Municipality'])

    if 'PostalCode' in address and address['PostalCode']:
        tags['addr:postcode'] = address['PostalCode']

    return tags


def capitalize_names(name):
    return ' '.join([x.capitalize() for x in name.split(' ')])


def user_agent():
    return 'Mozilla/5.0 (X11; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0'
