import os
from PIL import Image
import timeit


def find_most_common_color(image):
    image = Image.open(image)
    width, height = image.size
    # find pixel colors from image
    pixel = image.getcolors(width * height)
    # find most common color
    common_color = max(pixel, key=lambda t: t[0])
    return common_color[1]


if __name__ == "__main__":
    image = "data/islands_sprite_masks.png"
    print(find_most_common_color(image))
    # count time for function
    print(timeit.timeit(stmt=lambda: find_most_common_color(image), number=1))
