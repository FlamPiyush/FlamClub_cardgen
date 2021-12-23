import time

import PIL
import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def load_images_from_folder(folder):


    images = []
    for filename in os.listdir(folder):

        try:
            img = Image.open(os.path.join(folder, filename))
        except Exception as e:
            print(e)
            img = None
        if img is not None:
            images.append(img)

    print("images Loaded from folder")

    return images


def generate_black_code_image(width, height, code, font_size=36, font_type="f.ttf"):

    black_image = Image.new('RGBA', (width, height), (0, 0, 0, 255))
    font = ImageFont.truetype(font_type, font_size)
    font.set_variation_by_name("Bold")
    d1 = ImageDraw.Draw(black_image)

    w, h = d1.textsize(str(code), font=font)
    d1.text(((width - w) / 2, (height - 1.5 * h) / 2), str(code), fill=(255, 255, 255, 255), font=font)

    return black_image


def generate_image(seed, folder_name, code, text_width=500, text_height=100, width=900, height=1600, m=100, k=200, base_height=100, th=50, density=200, font_size=56, font_type="f.ttf"):

    print("Starting FlamClub Algo................................")
    print("Default value of width == 900....")
    print("Default value of height == 1600..")
    print("Default value of margin in width == 200....")
    print("Default value of margin in height == 100....")
    print("Default value of doodle height == 100....")
    print("Default value of distance b/w doodle == 50....")
    print("Default value of density of doodles == 200....")
    images = load_images_from_folder(folder_name)

    res_images = []
    start = time.time()

    for img in images:
        if img.size[0] > img.size[1]:
            width_percent = (base_height / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(width_percent)))
            a = base_height
        else:
            hsize = base_height
            width_percent = (base_height / float(img.size[1]))
            a = int((float(img.size[0]) * float(width_percent)))

        try:

            img = img.resize((a, hsize), Image.ANTIALIAS)
            res_images.append(img)

        except Exception as e:
            print(e)
    end = time.time()
    print(end - start)

    points = []

    random.seed(seed)
    for i in range(density):
        _x = random.randint(0, width - m)
        _y = random.randint(0, height - k)
        add = True
        for j in points:
            dist = np.linalg.norm(np.array(j) - np.array((_x, _y)))
            if dist < th:
                add = False
                break
            pass
        if add:
            points.append((_x, _y))

    transparent_image = Image.new('RGBA', (width, height), (0, 0, 0, 255))

    new_image = transparent_image.copy()

    random.seed(seed)
    for i in points:
        a = random.randint(0, 360)
        var = random.randint(0, len(res_images) - 1)
        put_shapes = res_images[var]
        put_shapes = put_shapes.rotate(a, PIL.Image.NEAREST, expand=True)
        new_image.paste(put_shapes, i, put_shapes)

    mid_image = generate_black_code_image(text_width, text_height, code, font_size, font_type)

    text_h = int((new_image.size[1] - mid_image.size[1] * 1) / 2)
    text_w = int((new_image.size[0] - mid_image.size[0] * 1) / 2)

    print(text_w, text_h)

    new_image.paste(mid_image, (text_w, text_h), mid_image)
    new_image.show()

    new_image.save("New{}{}{}.png".format(seed, th, base_height))


generate_image(123123123, "shapes", 353453)
