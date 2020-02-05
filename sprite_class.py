class Sprite():
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


# # Example Invalid cordinate
# sprite = Sprite(1, -1, 0, 0, 0)
# print(sprite)

# sprite = Sprite(1, "Hello", 0, 0, 0)
# print(sprite)

# # Example valid cordinate
# sprite = Sprite(1, 12, 23, 145, 208)
# print(sprite.label)
# print(sprite.width)
# print(sprite.height)
# print(sprite.top_left)
# print(sprite.bottom_right)

# sprite = Sprite(8, 55, 88, 457, 124)
# print(sprite.label)
# print(sprite.width)
# print(sprite.height)
# print(sprite.top_left)
# print(sprite.bottom_right)