from PIL import Image

def change_size_mode_image(image_path):
    image = Image.open(image_path)
    image.thumbnail((1800, 1800))
    if image.mode in ["RGBA", "P"]:
        image = image.convert('RGB')
    image.save(f'{image_path}', format('JPEG'))
