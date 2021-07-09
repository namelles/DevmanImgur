from os import listdir
from PIL import Image


def change_image_size(image_path):
    max_image_size = (1800, 1800)
    image = Image.open(image_path)
    image.thumbnail(max_image_size)
    image.save(image_path)


def change_image_mode(image_path):
    image = Image.open(image_path)
    if image.mode in ["RGBA", "P"]:
        image = image.convert('RGB')
    image.save(image_path)


def reformat_images(img_catalog_path):
    image_names = listdir(img_catalog_path)
    images = filter(lambda filename: filename.endswith('.jpg'), image_names)
    for image in images:
        image_path = f'{img_catalog_path}{image}'
        change_image_mode(image_path)
        change_image_size(image_path)
