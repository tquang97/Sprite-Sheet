from PIL import Image
import numpy as np

def image_segmentation(rows, cols, image_map, label_map, connection, background):
    """
    Sprites correspond to smaller images composed of connected pixels, 
    meaning that each pixel of a sprite is adjacent to at least one of its direct neighbor pixels 
    (8-neighborhood connectivity method)
    rows, cols: cordinates of image
    image_map: an image
    label_map: label of image, return '1'
    conntection: connectivity of each pixel in image
    background: image's background, return '0'
    """
    label = 1
    for x in range(rows):
        for y in range(cols):
            if np.array_equal(image_map[x][y], background):
                continue
            for i, j in [[x, y-1], [x-1, y-1], [x-1, y], [x-1, y]]:
                if (i, j) < (0, 0) or (i, j) > (rows, cols):
                    continue
                if label_map[i][j] != 0:
                    if label_map[x][y] == 0:
                        label_map[x][y] = label_map[i][j]
                    elif label_map[x][y] != label_map[i][j]:
                        connection[label_map[i][j]].append(label_map[x][y])
                        break
            else:
                if not label_map[x][y]:
                    label_map[x][y] = label
                    connection[label] = []
                    label += 1
    return True


def connect_segmentation(connect, list_connections):
    for x in reversed(list_connections):
        count = 0
        try:
            connect[x] = list(set(connect[x]))
            while count < len(connect[x]):
                connect[x] += connect[connect[x][count]]
                connect[x] = list(set(connect[x]))
                count += 1
        except (IndexError):
            continue
    return True


def images_composed(connect, list_key_connection):
    for index1, key in enumerate(list_key_connection[:-1]):
        for _, key2 in enumerate(list_key_connection[index1+1:], index1+1):
            new_list = connect[key2] + [key2]
            if any(x in connect[key] for x in new_list):
                connect[key] += new_list
                connect[key] = list(set(connect[key]))
                connect[key2].clear()

    return {k: v for k, v in connect.items() if v}
