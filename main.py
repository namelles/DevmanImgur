import urllib.parse

import requests
import os
from PIL import Image
from urllib.parse import urlparse


def download_spacex_images(url):
    img_catalog_path = 'images/'
    response = requests.get(url)
    response.raise_for_status()
    image_name = os.path.split(urlparse(url).path)[1]
    print(image_name)
    with open(f'{img_catalog_path}{image_name}', 'wb') as file:
        file.write(response.content)


def get_spacex_images_urls(limit_starts, starts_number):
    url = 'https://api.spacexdata.com/v3/launches'
    params = {
        'limit': limit_starts,
        'offset': starts_number
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()[0]['links']['flickr_images']


def fetch_spacex_launch(url):
    for urls in url:
        download_spacex_images(urls)


def get_hubble_images_urls(image_id):
    url = f'http://hubblesite.org/api/v3/image/{image_id}'
    response = requests.get(url)
    response.raise_for_status()
    image_url = []
    for url in response.json()['image_files']:
        image_url.append(f"https:{url['file_url']}")
    return image_url[-1]


def get_hubble_collection_images_id(collection_name):
    url = f'https://hubblesite.org/api/v3/images/{collection_name}'
    params = {
        'page': 'all'
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    images_id = []
    for image_id in response.json():
        images_id.append(image_id['id'])
    return images_id


def get_file_extension(url):
    image_extension = os.path.splitext(urlparse(url).path)[1]
    return image_extension


def download_hubble_images(image_id):
    img_catalog_path = 'images/'
    response = requests.get(get_hubble_images_urls(image_id), verify=False)
    image_name = f'{image_id}{get_file_extension(get_hubble_images_urls(image_id))}'
    with open(f'{img_catalog_path}{image_name}', 'wb') as file:
        file.write(response.content)


def download_hubble_collection_images(images_id):
    for image_id in images_id:
        response = requests.get(get_hubble_images_urls(image_id), verify=False)
        image_name = f'{image_id}{get_file_extension(get_hubble_images_urls(image_id))}'
        with open(f'{img_catalog_path}{image_name}', 'wb') as file:
            file.write(response.content)
        resize_image(f'{img_catalog_path}{image_name}')


def resize_image(image_path):
    image = Image.open(image_path)
    image.thumbnail((1800, 1800))
    if image.mode in ["RGBA", "P"]:
        image = image.convert('RGB')
    image.save(f'{image_path}', format('JPEG'))


if __name__ == '__main__':
    image_name = 'hubble.jpeg'
    img_catalog_path = 'images/'
    limit_starts = 1
    starts_number = 100
    image_id = '50'
    os.makedirs(img_catalog_path, exist_ok=True)
    url = 'https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg'
    collection_name = 'holiday_cards'
    download_hubble_collection_images(get_hubble_collection_images_id(collection_name))

