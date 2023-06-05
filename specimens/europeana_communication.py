from urllib import parse
import base64
import requests
import random
from django.conf import settings
from specimens.open_api_communication import get_openai_data

BASE_URL = "https://api.europeana.eu/record/v2/search.json"
API_KEY = settings.EUROPEANA_KEY


def parse_data(data, only_one):
    elements = [format_element(i) for i in data.get('items', []) if valid_element(i)]
    if not only_one:
        return elements
    return get_random_element(elements) if elements else empty_element()


def format_element(item):
    element_name = item['dcTitleLangAware'].get('la') or item['dcTitleLangAware'].get('def')
    element_name = element_name[0] if isinstance(element_name, list) else element_name
    image = item.get('edmPreview', [None])[0] or item['edmIsShownBy'][0]
    data = {'name': f"{element_name} - {item.get('dataProvider', ['Unknown'])[0]}", 'image': image}
    print(item.get('edmPreview', [None])[0])
    return data


def valid_element(item):
    return item.get('dcTitleLangAware') and item.get('edmIsShownBy')


def get_random_element(elements):
    random_element = random.choice(elements)
    name = random_element.get('name')
    image_as_b64 = base64.b64encode(requests.get(random_element['image']).content).decode('utf-8')
    google_response = requests.get(f'https://customsearch.googleapis.com/customsearch/v1?cx=001928687561571394193%3At_qhgoibaiq&num=2&q={parse.quote(name)}%20description&key={settings.GOOGLE_API_KEY}')
    description = get_openai_data([{'role': 'user', 'content': f"A person took a picture of a {name} google returned {google_response.json()}, extract the description from here and summarize it up to 50 words I need description of the thing. Take the risk no explanations just the description. And do not mention anything about search results and dont mention google."}])

    return {
        'name': name,
        'image': image_as_b64,
        'description': description
    }


def empty_element():
    return {'name': '', 'image': '', 'description': ''}


def get_data_from_europeana(lat, lon, only_one=True):
    lat, lon = round(lat, 1), round(lon, 1)
    random_value_lat, random_value_lon = random.uniform(0.1, 2.5), random.uniform(0.1, 2.5)
    query_params = {
        "qf": f"pl_wgs84_pos_lat:[{lat} TO {lat + random_value_lat}] AND pl_wgs84_pos_long:[{lon} TO {lon + random_value_lon}]",
        "query": "PROVIDER:(OpenUp!)",
        "rows": "5",
        "start": "1",
        "wskey": API_KEY
    }
    response = requests.get(f"{BASE_URL}?{parse.urlencode(query_params)}")
    response.raise_for_status()  # raises an HTTPError if the response status is 4xx, 5xx
    return parse_data(response.json(), only_one=only_one)
