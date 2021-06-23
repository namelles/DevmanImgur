import requests
import os
from PIL import Image
from urllib.parse import urlparse


def download_spacex_images(url):
    img_catalog_path = 'images/'
    response = requests.get(url)
    response.raise_for_status()
    image_name = os.path.split(urlparse(url).path)[1]
    with open(f'{img_catalog_path}{image_name}', 'wb') as file:
        file.write(response.content)
    resize_image(f'{img_catalog_path}{image_name}')


def get_spacex_images_urls(spacex_starts_number):
    url = 'https://api.spacexdata.com/v3/launches'
    limit_starts = 1
    params = {
        'limit': limit_starts,
        'offset': spacex_starts_number
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()[0]['links']['flickr_images']


def download_spacex_launch_images(spacex_starts_number):
    spacex_images_urls = get_spacex_images_urls(spacex_starts_number)
    for spacex_image_url in spacex_images_urls:
        download_spacex_images(spacex_image_url)


def resize_image(image_path):
    image = Image.open(image_path)
    image.thumbnail((1800, 1800))
    if image.mode in ["RGBA", "P"]:
        image = image.convert('RGB')
    image.save(f'{image_path}', format('JPEG'))
