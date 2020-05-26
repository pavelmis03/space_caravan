import unittest

from geometry.circle import Circle
from geometry.distances import dist, dist_point_line
from geometry.line import Line, line_from_points, point_on_line
from geometry.point import Point
from geometry.segment import Segment, point_on_segment


class TestCircle(unittest.TestCase):

    def setUp(self):
        self.circle = Circle(Point(0, 0), 10)

    def test_is_inside1(self):
        """ Test inside circle """
        result = self.circle.is_inside(Point(4, 9))
        self.assertTrue(result)

    def test_is_inside2(self):
        """ Test negative coords """
        result = self.circle.is_inside(Point(4, -9))
        self.assertTrue(result)

    def test_is_inside3(self):
        """ Test outside circle """
        result = self.circle.is_inside(Point(4, 11))
        self.assertFalse(result)


class TestLine(unittest.TestCase):

    def setUp(self):
        self.line = Line(2, -1, 1)

    def test_normal(self):
        result = self.line.get_normal()
        self.assertEqual(result, Point(2, -1))

    def test_parallel(self):
        result = self.line.get_parallel()
        self.assertEqual(result, Point(-1, -2))

    def test_line_from_points(self):
        result = line_from_points(Point(0, 1), Point(1, 3))
        self.assertEqual(result, self.line)

    def test_p_on_line1(self):
        """ Test if point on line really on line """
        result = point_on_line(Point(0, 1), self.line)
        self.assertTrue(result)

    def test_p_on_line2(self):
        """ Test if point is not on line really not on line """
        result = point_on_line(Point(3, 6), self.line)
        self.assertFalse(result)


class TestDistances(unittest.TestCase):

    def setUp(self):
        self.p = Point(1, 1)

    def test_dist_p2p(self):
        """ Test distance between points """
        result = dist(self.p, Point(4, 5))
        self.assertEqual(result, 5)

    def test_dist_p2l(self):
        """ Test distance between line and point """
        result = dist_point_line(self.p, Line(1, 0, 2)) # y = 2
        self.assertEqual(result, 3)


class TestSegments(unittest.TestCase):

    def setUp(self):
        self.segment = Segment(Point(1, 1), Point(4, 5))

    def test_length(self):
        result = self.segment.length
        self.assertEqual(result, 5)

    def test_p_on_seg1(self):
        """ Test if point on segment really on segment """
        result = point_on_segment(Point(1, 1), self.segment)
        self.assertTrue(result)

    def test_p_on_seg2(self):
        """ Test if point not on segment really not on segment """
        result = point_on_segment(Point(-2, -3), self.segment)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
