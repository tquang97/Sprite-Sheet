import os
from PIL import Image
import timeit


def find_most_common_color(image):
    """
    Find pixel color that is the most commond use in image
    image: an Image object
    return: the most commond color in image
    """
    image = Image.open(image)
    width, height = image.size
    # find pixel colors from image
    pixel = image.getcolors(width * height)
    
    # find most common color
    common_color = max(pixel, key=lambda t: t[0])
    return common_color[1]
    

def image_mode(image):
    image = Image.open(image)
    mode = image.mode
    return mode

if __name__ == "__main__":
    image = "data/islands_sprite_masks.png"
    print(find_most_common_color(image))
    print(image_mode(image))
    # count time for function
    print(timeit.timeit(stmt=lambda: find_most_common_color(image), number=1))
