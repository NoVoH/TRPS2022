import sys
from typing import List

from coffee_central import Simulator, Point

MIN_GRID_SIZE = 1
MAX_GRID_SIZE = 1000
GRID_SIZE_BOUNDS = f'[{MIN_GRID_SIZE} .. {MAX_GRID_SIZE}]'

MIN_SHOP_COUNT = 0
MAX_SHOP_COUNT = 5105
SHOP_COUNT_BOUNDS = f'[{MIN_SHOP_COUNT} .. {MAX_SHOP_COUNT}]'

MIN_QUERY_COUNT = 1
MAX_QUERY_COUNT = 20
QUERY_COUNT_BOUNDS = f'[{MIN_QUERY_COUNT} .. {MAX_QUERY_COUNT}]'

MIN_WALK_DISTANCE = 0
MAX_WALK_DISTANCE = 106
WALK_DISTANCE_BOUNDS = f'[{MIN_WALK_DISTANCE} .. {MAX_WALK_DISTANCE}]'

POSITION_OUTPUT_OFFSET = Point(1, 1)

EXIT_FAIL = 1


def main(argv):
    f = sys.stdin
    case_number = 1
    while True:
        l = f.readline()
        if l is None:
            print('Unexpected EOF, cases list should be followed by line',
                  'of 4 zeros separated with whitespace')
            return EXIT_FAIL

        l = l.split()
        try:
            if len(l) < 4:
                raise ValueError()
            dx, dy, shop_count, query_count = map(int, l)
        except ValueError:
            print('First line of each case should contain 4 integers:',
                  'city grid dimensions, coffee chop and query counts')
            return EXIT_FAIL

        if dx == dy == shop_count == query_count == 0:
            break

        print(f'\nCase {case_number}:')

        if not (MIN_GRID_SIZE <= dx <= MAX_GRID_SIZE
                and MIN_GRID_SIZE <= dy <= MAX_GRID_SIZE):
            print(f'City grid dimensions {dx}x{dy} are not within allowed',
                  'range:', GRID_SIZE_BOUNDS)
            return EXIT_FAIL

        if not (MIN_SHOP_COUNT <= shop_count <= MAX_SHOP_COUNT):
            print(f'Shop count {shop_count} is not within allowed range:',
                  SHOP_COUNT_BOUNDS)
            return EXIT_FAIL

        if not (MIN_QUERY_COUNT <= query_count <= MAX_QUERY_COUNT):
            print(f'Query count {query_count} is not within allowed range:',
                  QUERY_COUNT_BOUNDS)
            return EXIT_FAIL

        shops: List[Point] = []
        for i in range(shop_count):
            l = f.readline()
            if l is None:
                print(f'Unexpected EOF, shop list should have {shop_count}',
                      'lines with shop coordinates')
                return EXIT_FAIL
            try:
                shop_x, shop_y = map(int, l.split())
            except ValueError:
                print('Each line in shop list should contain 2 integers - shop',
                      'coordinates')
                return EXIT_FAIL
            if not (MIN_GRID_SIZE <= shop_x <= dx
                    and MIN_GRID_SIZE <= shop_y <= dy):
                print(f'Shop coordinates ({shop_x}, {shop_y}) are outside of',
                      'the city bounds or in the wrong order')
                return EXIT_FAIL
            shops.append(Point(shop_x - 1, shop_y - 1))

        queries: List[int] = []
        for i in range(query_count):
            l = f.readline()
            if l is None:
                print(f'Unexpected EOF, query list should have {query_count}',
                      'lines with maximum walk distances')
                return EXIT_FAIL
            try:
                query = int(l)
            except ValueError:
                print('Each line in query list should contain integer -',
                      'maximum walk distance for the query')
                return EXIT_FAIL
            if not (MIN_WALK_DISTANCE <= query <= MAX_WALK_DISTANCE):
                print(f'Walk distance {query} is not within allowed range:',
                      WALK_DISTANCE_BOUNDS)
                return EXIT_FAIL
            queries.append(query)

        s = Simulator(dx, dy, shops, queries)
        best_locations = s.run()
        for l in best_locations:
            print(l.shop_count, l.position + POSITION_OUTPUT_OFFSET)
        case_number += 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
