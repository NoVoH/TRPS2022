import dataclasses
from typing import List

from .field import Field
from .point import Point


@dataclasses.dataclass
class OptimalLocation:
    shop_count: int = 0
    position: Point = dataclasses.field(default_factory=Point)


class Simulator:
    def __init__(self, city_width: int, city_length: int, shops: List[Point], queries: List[int]):
        self._shops = Field(city_width, city_length, 0)
        for s in shops:
            self._shops[s.x, s.y] += 1
        self._queries = queries

    def run(self)-> List[OptimalLocation]:
        result = [
            self._find_optimal_location(radius)
            for radius in self._queries
        ]
        return result

    def _find_optimal_location(self, radius):
        location = OptimalLocation()
        for y in range(self._shops.height):
            for x in range(self._shops.width):
                if self._shops[x, y] > 0:
                    continue
                p = Point(x, y)
                local_count = self._get_shop_count(radius, x, y)
                if location.shop_count > local_count:
                    continue
                if local_count > location.shop_count or location.position > p:
                    location.shop_count = local_count
                    location.position = p
        return location

    def _get_shop_count(self, radius, x, y):
        shop_count = 0
        for neighbour in self._shops.iterate_4_neighbourhood(x, y, radius):
            shop_count += self._shops[neighbour]
        return shop_count


