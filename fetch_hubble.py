import os
from urllib.parse import urlparse

import requests


def get_hubble_image_url(image_id):
    url = f'http://hubblesite.org/api/v3/image/{image_id}'
    response = requests.get(url)
    response.raise_for_status()
    return f"https:{response.json()['image_files'][-1]['file_url']}"


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


def download_hubble_collection_images(collection_name, img_catalog_path):
    images_id = get_hubble_collection_images_id(collection_name)
    for image_id in images_id:
        image_url = get_hubble_image_url(image_id)
        response = requests.get(image_url, verify=False)
        image_name = f'{image_id}{get_file_extension(image_url)}'
        with open(f'{img_catalog_path}{image_name}', 'wb') as file:
            file.write(response.content)
