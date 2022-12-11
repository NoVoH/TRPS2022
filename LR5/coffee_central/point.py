import dataclasses


@dataclasses.dataclass
class Point:
    x: int = 0
    y: int = 0

    def clone(self):
        return dataclasses.replace(self)

    def __add__(self, other: 'Point'):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Point'):
        return Point(self.x - other.x, self.y - other.y)

    def __lt__(self, other: 'Point'):
        return self.y < other.y or (self.y == other.y and self.x < other.x)

    def __le__(self, other: 'Point'):
        return self.y < other.y or (self.y == other.y and self.x <= other.x)

    def __str__(self):
        return f'({self.x},{self.y})'
