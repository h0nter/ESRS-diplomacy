# Create your tests here.
from django.test import TestCase
from .game.only_test import SimpleTest

class room_app_unitTest1(TestCase):
    def test_simpleMethod(self):
        SimpleTest()
