# Create your tests here.
from django.test import TestCase

class room_app_unitTest1(TestCase):
    def test_insert(self):
        from .initial_insert import InitialInsert as II
        II.all_insert()

