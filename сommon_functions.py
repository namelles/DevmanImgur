from PIL import Image

IMG_CATALOG_PATH = 'images/'

def change_size_mode_image(image_path):
    max_size_image = (1800, 1800)
    image = Image.open(image_path)
    image.thumbnail(max_size_image)
    if image.mode in ["RGBA", "P"]:
        image = image.convert('RGB')
    image.save(image_path, format('JPEG'))
