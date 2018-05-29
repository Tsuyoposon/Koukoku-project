import numpy as np


class QuadraticEquation(object):
    """Quadratic equation class
    """

    def __init__(self):
        self.a = 1.0
        self.b = 2.0
        self.c = 1.0

    def calc_root(self):
        """calculate root

        :return: root1, root2 (root1 < root2)
        """
        x1 = (-1.0 * self.b - np.sqrt(self.b * self.b - 4.0 * self.a * self.c)) / (2.0 * self.a)
        x2 = (-1.0 * self.b + np.sqrt(self.b * self.b - 4.0 * self.a * self.c)) / (2.0 * self.a)
        return x1, x2

    def calc_value(self, x):
        """ calculate polynomial value

        :param x: x
        :return: a * x^2 + b * x + c
        """

        return self.a * np.power(x, 2.0) + self.b * x + self.c
