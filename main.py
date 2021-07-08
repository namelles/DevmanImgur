import argparse
import os
from datetime import datetime
from os import listdir

from dotenv import load_dotenv
from imgurpython import ImgurClient

from fetch_spacex import download_spacex_launch_images
from fetch_hubble import download_hubble_collection_images
from reformat_images import reformat_images


def authenticate_imgur(client_id, client_secret):
    client = ImgurClient(client_id, client_secret)
    authorization_url = client.get_auth_url('pin')
    print("Go to the following URL: {0}".format(authorization_url))
    pin = input("Enter pin code: ")
    credentials = client.authorize(pin, 'pin')
    client.set_user_auth(credentials['access_token'],
                         credentials['refresh_token'])
    print("Authentication successful! Here are the details:")
    print("   Access token:  {0}".format(credentials['access_token']))
    print("   Refresh token: {0}".format(credentials['refresh_token']))
    return client


def upload_images_imgur(client, img_catalog_path):
    album = None
    name_images = listdir(img_catalog_path)
    images = filter(lambda x: x.endswith('.jpg'), name_images)
    for image in images:
        config = {
            'album': album,
            'name': image,
            'title': image,
            'description': 'Devman {0}'.format(datetime.now())
        }
        image_path = f'{img_catalog_path}{image}'
        image = client.upload_from_path(image_path, config=config, anon=False)


def create_argument_parser():
    parser = argparse.ArgumentParser(description="""Upload SpaceX and Hubble
                                     images to Imgur service.""")
    parser.add_argument('--start_number', default='100',
                        help='Set start number of SpaceX')
    parser.add_argument('--collection', default='holiday_cards',
                        help='Set Hubble photo collection. Example "holiday_cards"')
    return parser


if __name__ == '__main__':
    load_dotenv()
    img_catalog_path = 'images/'
    os.makedirs(img_catalog_path, exist_ok=True)
    parser = create_argument_parser()
    args = parser.parse_args()
    collection_name = args.collection
    spacex_start_number = args.start_number
    imgur_client_id = os.getenv('IMGUR_CLIENT_ID')
    imgur_client_secret = os.getenv('IMGUR_CLIENT_SECRET')
    download_spacex_launch_images(spacex_start_number, img_catalog_path)
    download_hubble_collection_images(collection_name, img_catalog_path)
    reformat_images(img_catalog_path)
    upload_images_imgur(authenticate_imgur(imgur_client_id, imgur_client_secret), img_catalog_path)
