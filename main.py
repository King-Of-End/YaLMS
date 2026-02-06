import sys
from io import BytesIO
from get_map_params import get_maps_params

import requests
from PIL import Image


def get_toponym():
    toponym_to_find = " ".join(sys.argv[1:])
    if not toponym_to_find:
        toponym_to_find = input('Введите адрес для поиска\n')
    if not toponym_to_find:
        toponym_to_find = 'Барклая 5А'

    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
        "geocode": toponym_to_find,
        "format": "json",
    }

    response = requests.get(geocoder_api_server, params=geocoder_params)

    json_response = response.json()
    return json_response


def main():
    json_response = get_toponym()
    map_params = get_maps_params(json_response)
    map_api_server = "https://static-maps.yandex.ru/v1"
    response = requests.get(map_api_server, params=map_params)
    im = BytesIO(response.content)
    opened_image = Image.open(im)
    opened_image.show()


if __name__ == '__main__':
    main()
