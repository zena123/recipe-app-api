from django.test import TestCase
from app.calc import add

#always start test functions with name = test ,else error
class CalcTests(TestCase):
    def test_add_numbers(self):
        """ to test add two numbers function"""
        self.assertEqual(add(3,8),11)