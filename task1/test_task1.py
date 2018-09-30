import unittest

from .task_1 import function, func2


class TestCase(unittest.TestCase):
    def test_function(self):
        self.assertEquals(function(2, 3), 5)
    def test_function2(self):
        self.assertEquals(func2(5, 6), 1)
