from os import listdir

from PIL import Image


def change_size_image(image_path):
    max_size_image = (1800, 1800)
    image = Image.open(image_path)
    image.thumbnail(max_size_image)
    image.save(image_path, format('JPEG'))


def change_mode_image(image_path):
    image = Image.open(image_path)
    if image.mode in ["RGBA", "P"]:
        image = image.convert('RGB')
    image.save(image_path, format('JPEG'))


def reformat_images(img_catalog_path):
    name_images = listdir(img_catalog_path)
    images = filter(lambda x: x.endswith('.jpg'), name_images)
    for image in images:
        image_path = f'{img_catalog_path}{image}'
        change_mode_image(image_path)
        change_size_image(image_path)
