import os
import urllib.parse

import requests


def download_spacex_image(url, img_catalog_path):
    response = requests.get(url)
    response.raise_for_status()
    url_path = urllib.parse.urlsplit(url)[2]
    image_name = os.path.split(urllib.parse.unquote(url_path))[1]
    with open(f'{img_catalog_path}{image_name}', 'wb') as file:
        file.write(response.content)


def get_spacex_images_urls(spacex_start_number):
    url = f'https://api.spacexdata.com/v3/launches/{spacex_start_number}'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()[0]['links']['flickr_images']


def download_spacex_launch_images(spacex_starts_number, img_catalog_path):
    spacex_image_urls = get_spacex_images_urls(spacex_starts_number)
    for spacex_image_url in spacex_image_urls:
        download_spacex_image(spacex_image_url, img_catalog_path)
