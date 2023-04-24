# Create your tests here.
from django.test import TestCase

# https://docs.djangoproject.com/en/4.1/topics/testing/tools/#django.test.TestCase 
class room_app_test_resolve_orders(TestCase):
    # setup test database to use throughout this class
    @classmethod
    def setUpTestData(cls):
        pass