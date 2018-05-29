import unittest
import QuadraticEquation
from unittest import TestCase


class TestQuadraticEquation(unittest.TestCase):
    def setUp(self):
        print("setup")
        self.eq = QuadraticEquation.QuadraticEquation()

    def test_calc_root(self):
        """ test method of s"""
        expected = (-1.0, -1.0)
        actual = self.eq.calc_root()

        self.assertEqual(expected, actual)
        self.assertEqual((0.0, 0.0), (self.eq.calc_value(actual[0]), self.eq.calc_value(actual[1])))

    def test_calc_value(self):
        """ test method of calc_value() """
        expected = (4.0, 9.0)
        actual = (self.eq.calc_value(1.0), self.eq.calc_value(2.0))

        self.assertEqual(expected, actual)

    def tearDown(self):
        print("tearDown") 
        del self.eq


if __name__ == '__main__':
    unittest.main()
