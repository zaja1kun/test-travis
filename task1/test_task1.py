import unittest

from .task_1 import function


class TestCase(unittest.TestCase):
    def test_function(self):
        self.assertEquals(function(2, 3), 5)
