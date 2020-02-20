from PIL import Image, ImageDraw
import numpy as np
import timeit

def find_most_common_color(image):
    """
    Find pixel color that is the most commond use in image
    image: an Image object
    return: the most commond color
    """
    width, height = image.size
    # find pixel colors from image
    pixel = image.getcolors(width * height)
    
    # find most common color
    common_color = max(pixel, key=lambda t: t[0])
    return common_color[1]
    

def image_mode(image):
    """
    Show mode of image is 'RGB' or 'RGBA'
    image: an Image object
    return: mode
    """
    mode = image.mode
    return mode


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


def connect_segmentation(connect, list_connections):
    """
    connect label like:
    connect = {             connect = {
        1: {2,3,4}              1 : {2,3,4,5,6,7,8,9}
        2: {5,6}        =>  }
        3: {7,8,9}
    }
    @param connect : dict contain all pixels label and sprite's label that key belong to
    @param list_key_connect : list contain all key label in dict connect
    """
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


def images_composed(connect, list_connections):
    """
    combine labels with the same connection
    @param connect : dict contain all pixels label and sprite's label that key belong to
    @param list_connections : list contain all key label in dict connect
    @return a dict contain label and sprite's label that key belong to
    """
    for index1, key in enumerate(list_connections[:-1]):
        for _, key2 in enumerate(list_connections[index1+1:], index1+1):
            new_list = connect[key2] + [key2]
            if any(x in connect[key] for x in new_list):
                connect[key] += new_list
                connect[key] = list(set(connect[key]))
                connect[key2].clear()

    return {k: v for k, v in connect.items() if v}


def find_sprites(image, background=None):
    """ 
    Detect sprites inside the image
    Return a 2D label map and a dict that stores:
            key: sprite's label
            value: its Sprite's object
 vim  __init__.py   """
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


background_color=(255, 255, 255)

def create_sprite_labels_image(srpite, label_map):
    """
        Draws the masks of the sprites at the exact same position that the sprites were in the original image.
        Returns an image of equal dimension (width and height) as the original image that was passed to the function
    """
    if len(background_color) == 4:
        color_mode, c = ('tuple(np.random.randint(256, size=3)) + (255,)', 3)
    else:
        color_mode, c = ('tuple(np.random.randint(256, size=3))', 2)
    color = {}
    color[0] = background_color
    zeros_array = np.zeros((*label_map.shape, c), dtype=int)
    label_map = np.expand_dims(label_map, axis=2)
    label_map = np.append(label_map, zeros_array, axis=2)

    coordinate = np.argwhere(np.all(label_map == [0, *[0]*c], axis=2))
    for x, y in coordinate:
        label_map[x][y] = color[0]

    for x in srpite.keys():
        color[x] = eval(color_mode)
        coordinate = np.argwhere(np.all(label_map == [x, *[0]*c], axis=2))
        for i, j in coordinate:
            label_map[i][j] = color[x]

    
    image = Image.fromarray(label_map.astype('uint8'))
    draw = ImageDraw.Draw(image)
    for x, y in srpite.items():
        draw.rectangle((y.top_left, y.bottom_right), outline=color[x])

    return image

class Sprite():
    """
    Class sprite that show label, width, height, top_left and bottom right of image
    label: Image's labe
    x1, x2, y1, y2: cordinates of image
    """
    def __init__(self, label, x1, y1, x2, y2):
        if any(not isinstance(i, int) for i in [x1, x2, y1, y2]):
            raise ValueError('Invalid coordinates')
        elif any(i < 0 for i in [x1, x2, y1, y2]) :
            raise ValueError('Invalid coordinates')
        elif (x2, y2) <= (x1, y1):
            raise ValueError('Invalid coordinates')
        self._label = label
        self._width = x2 - x1 + 1
        self._height = y2 - y1 + 1
        self._top_left = (y1, x1)
        self._bottom_right = (y2, x2)
        
        
    @property
    def label(self):
        return self._label
    @property
    def width(self):
        return self._width
    @property
    def height(self):
        return self._height
    @property
    def top_left(self):
        return self._top_left
    @property
    def bottom_right(self):
        return self._bottom_right


class SpriteSheet:
    def __init__(self, fd, background=None):
        self.fd = self.__image_obj(fd)
        if background:
            self._background_color = background
        else:
            self._background_color = SpriteSheet.find_most_common_color(self.fd)
        self.__label_map = ''
        self.__sprites = ''
    
    @property
    def background_color(self):
        return self._background_color

    def __image_obj(self, fd):
        try:
            return Image.open(fd)
        except (AttributeError, UnicodeDecodeError):
            try:
                return Image.open(fd.name)
            except Exception:
                return fd

    @staticmethod
    def find_most_common_color(image):
        """
        Get the pixel color that is the most used in this image
        @param image : a Image object
        @return : most common color in image
        """
        return find_most_common_color(image)
    
    
    def find_sprites(self):
        """ 
        Detect sprites inside the image
        Return a 2D label map and a dict that stores:
                key: sprite's label
                value: its Sprite's object
        """
        return find_sprites(self.fd)

    def create_sprite_labels_image(self):
        """
        Draws the masks of the sprites at the exact same position that the sprites were in the original image.
        Returns an image of equal dimension (width and height) as the original image that was passed to the function
        """
        sprites, label_map = self.find_sprites()
        # random color base on mode color (RGBA/RGB)
        return create_sprite_labels_image(sprites, label_map)


def main():
    obj = SpriteSheet('../data/optimized_sprite_sheet.png')
    create_obj = obj.create_sprite_labels_image().save('new.png')
    print(timeit.timeit(stmt=lambda: create_obj, number=1))
    # sprites, label_map = obj.find_sprites()
    # for label, sprite in sprites.items():
    #     s = (f"Sprite ({label}): [{sprite.top_left}, {sprite.bottom_right}] {sprite.width}x{sprite.height}")
    #     print(s)
    # print(timeit.timeit(stmt=lambda: s, number=1))

if __name__ == '__main__':
    main()
