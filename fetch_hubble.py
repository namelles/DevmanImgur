import requests
import os
from сommon_functions import change_size_mode_image
from urllib.parse import urlparse


def get_hubble_image_url(image_id):
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


def download_hubble_collection_images(collection_name):
    images_id = get_hubble_collection_images_id(collection_name)
    img_catalog_path = 'images/'
    for image_id in images_id:
        response = requests.get(get_hubble_image_url(image_id), verify=False)
        image_name = f'{image_id}{get_file_extension(get_hubble_image_url(image_id))}'
        with open(f'{img_catalog_path}{image_name}', 'wb') as file:
            file.write(response.content)
        change_size_mode_image(f'{img_catalog_path}{image_name}')
