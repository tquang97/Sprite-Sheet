from PIL import Image
import numpy as np
import pprint

from spriteutil import find_most_common_color, image_mode
from sprite_class import Sprite
from images_composed import image_segmentation, connect_segmentation, images_composed


def find_sprites(image, background=None):
    image_map = np.asarray(image)
    rows, cols = image_map.shape[:2]
    label_map = np.zeros((rows, cols))
    connection = {}

    if not background:
        if image.mode == 'RGBA':
            background = (0, 0, 0, 0)
        else:
            background = find_most_common_color(image)

    image_segmentation(rows, cols, image_map, label_map, connection, background)
    list_connections = list(connection.keys())

    connect_segmentation(connection, list_connections)
    connection = images_composed(connection, list_connections)

    sprites = {}

    for label, x in enumerate(connection, 1):
        for a in connection[x]:
            label_map[label_map == a] = label
        label_map[label_map == x] = label

        temp_array = np.argwhere(label_map == label)
        x_max, y_max = np.amax(temp_array, axis=0)
        x_min, y_min = np.amin(temp_array, axis=0)
        sprites[label] = Sprite(label, x_min.item(), y_min.item(), x_max.item(), y_max.item())

    return sprites, label_map

def main():
    image = Image.open('data/metal_slug_single_sprite_large.png')
    sprites, label_map = find_sprites(image)
    # pprint.pprint(label_map, width=120)
    array = np.array(label_map, dtype=np.int64) #dtype
    np.savetxt('label_result', label_map, fmt='%.0f')
    # print(len(sprites))
    # for label, sprite in sprites.items():
    #     print(f"Sprite ({label}): [{sprite.top_left}, {sprite.bottom_right}] {sprite.width}x{sprite.height}")

if __name__ == '__main__':
    main()