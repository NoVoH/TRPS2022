from typing import Iterable, Tuple


class Field:
    def __init__(self, width, height, default_value=None):
        self._width = width
        self._height = height
        self._data = [
            [default_value] * width
            for _ in range(height)
        ]

    def __getitem__(self, key):
        x, y = key
        return self._data[y][x]

    def __setitem__(self, key, value):
        """:key x, y coordinates"""
        x, y = key
        self._data[y][x] = value

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def reset(self, value):
        for y in range(self.height):
            for x in range(self.width):
                self._data[y][x] = value

    def iterate_4_neighbourhood(self, x: int, y: int, radius: int) -> Iterable[Tuple[int, int]]:
        for dy in range(radius):
            for dx in range(1, radius - dy + 1):
                if y >= dy and x >= dx:
                    yield x - dx, y - dy
                if y+dy < self.height and x+dx < self.width:
                    yield x + dx, y + dy
                if y+dx < self.height and x >= dy:
                    yield x - dy, y + dx
                if y >= dx and x+dy < self.width:
                    yield x + dy, y - dx
