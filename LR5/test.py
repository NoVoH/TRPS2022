#!/usr/bin/env python3

import unittest

from coffee_central import Simulator, Point
from coffee_central.field import Field


class TestPoint(unittest.TestCase):

    def setUp(self):
        self.point_1 = Point(4, 5)
        self.point_2 = Point(1, -2)
        self.point_3 = Point(4, 6)
        self.point_4 = Point(5, 5)
        self.point_5 = Point(4, -5)
        self.point_6 = Point(4, 5)

    def test_add(self):
        test_point = self.point_1 + self.point_2
        self.assertEqual(test_point.x, 5)
        self.assertEqual(test_point.y, 3)

    def test_sub(self):
        test_point = self.point_1 - self.point_2
        self.assertEqual(test_point.x, 3)
        self.assertEqual(test_point.y, 7)

    def test_str(self):
        self.assertEqual(str(self.point_1), "(4,5)")

    def test_cmp(self):
        try:
            self.assertTrue(self.point_1 <= self.point_1)
        except NotImplementedError:
            None
        try:
            self.assertFalse(self.point_1 < self.point_1)
            self.assertFalse(self.point_1 < self.point_2)
            self.assertTrue(self.point_1 < self.point_3)
            self.assertTrue(self.point_1 < self.point_4)
        except NotImplementedError:
            None

        try:
            self.assertTrue(self.point_1 >= self.point_1)
        except NotImplementedError:
            None

        try:
            self.assertFalse(self.point_1 > self.point_1)
            self.assertFalse(self.point_2 > self.point_1)
            self.assertTrue(self.point_3 > self.point_1)
            self.assertTrue(self.point_4 > self.point_1)
        except NotImplementedError:
            None

        try:
            self.assertFalse(self.point_1 == self.point_2)
            self.assertFalse(self.point_1 == self.point_5)
            self.assertTrue(self.point_1 == self.point_6)
        except NotImplementedError:
            None


class TestField(unittest.TestCase):

    def setUp(self):
        self.field = Field(100, 400, 0)

    def test_constructor(self):
        f = Field(0, 0, 0)
        self.assertEqual(len(f._data), 0)

        f = Field(1, 0, 0)
        self.assertEqual(len(f._data), 0)

        f = Field(0, 1, 0)
        self.assertEqual(len(f._data), 1)
        self.assertEqual(len(f._data[0]), 0)

        f = Field(3, 8, 4)
        self.assertEqual(f.width, 3)
        self.assertEqual(f.height, 8)
        for i in range(3):
            for k in range(8):
                self.assertEqual(f[i, k], 4)

        f = Field(8, 8)
        for i in range(8):
            for k in range(8):
                self.assertEqual(f[i, k], None)

    def test_getitem_setitem(self):
        self.field[3, 5] = 123456
        self.assertEqual(self.field[3, 5], 123456)

    def test_reset(self):
        self.field.reset(5)
        for i in range(self.field.width):
            for k in range(self.field.height):
                self.assertEqual(self.field[i, k], 5)

        self.field.reset(16)
        for i in range(self.field.width):
            for k in range(self.field.height):
                self.assertEqual(self.field[i, k], 16)

    def test_iterate_4_neighbourhood(self):
        result = list(self.field.iterate_4_neighbourhood(0, 0, 0))
        self.assertEqual(len(result), 0)

        result = list(self.field.iterate_4_neighbourhood(0, 0, 1))
        expected_result = [(1, 0), (0, 1)]
        self.assertEqual(len(result), len(expected_result))
        for pair in expected_result:
            self.assertTrue(pair in result)

        result = list(self.field.iterate_4_neighbourhood(self.field.width - 1, self.field.height - 1, 1))
        expected_result = [
            (self.field.width - 2, self.field.height - 1),
            (self.field.width - 1, self.field.height - 2)
        ]
        self.assertEqual(len(result), len(expected_result))
        for pair in expected_result:
            self.assertTrue(pair in result)

        result = list(self.field.iterate_4_neighbourhood(0, 0, 2))
        expected_result = [(1, 0), (0, 1), (2, 0), (0, 2), (1, 1)]
        self.assertEqual(len(result), len(expected_result))
        for pair in expected_result:
            self.assertTrue(pair in result)


class TestSimulator(unittest.TestCase):
    def test_simulation(self):
        s = Simulator(4, 4, [Point(0, 0), Point(0, 1), Point(2, 2), Point(3, 3), Point(1, 3)], [1, 2, 4])
        best_locations = s.run()
        self.assertEqual(len(best_locations), 3)
        self.assertEqual(best_locations[0].shop_count, 3)
        self.assertEqual(best_locations[0].position, Point(2, 3))
        self.assertEqual(best_locations[1].shop_count, 4)
        self.assertEqual(best_locations[1].position, Point(1, 1))
        self.assertEqual(best_locations[2].shop_count, 5)
        self.assertEqual(best_locations[2].position, Point(2, 0))

        s = Simulator(4, 4, [Point(0, 0), Point(0, 1), Point(2, 2), Point(3, 3), Point(1, 3)], [])
        best_locations = s.run()
        self.assertEqual(len(best_locations), 0)

        s = Simulator(0, 0, [], [])
        best_locations = s.run()
        self.assertEqual(len(best_locations), 0)


if __name__ == '__main__':
    unittest.main()
