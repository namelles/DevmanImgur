import os
import urllib.parse

import requests


def get_hubble_image_url(image_id):
    url = f'http://hubblesite.org/api/v3/image/{image_id}'
    response = requests.get(url)
    response.raise_for_status()
    return f"https:{response.json()['image_files'][-1]['file_url']}"


def get_hubble_collection_image_ids(collection_name):
    url = f'https://hubblesite.org/api/v3/images/{collection_name}'
    params = {
        'page': 'all'
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    images_ids = []
    for image_id in response.json():
        images_ids.append(image_id['id'])
    return images_ids


def get_file_extension(url):
    url_path = urllib.parse.urlsplit(url)[2]
    image_extension = os.path.splitext(urllib.parse.unquote(url_path))[1]
    return image_extension


def download_hubble_collection_images(collection_name, img_catalog_path):
    image_ids = get_hubble_collection_image_ids(collection_name)
    for image_id in image_ids:
        image_url = get_hubble_image_url(image_id)
        response = requests.get(image_url, verify=False)
        image_name = f'{image_id}{get_file_extension(image_url)}'
        with open(f'{img_catalog_path}{image_name}', 'wb') as file:
            file.write(response.content)
