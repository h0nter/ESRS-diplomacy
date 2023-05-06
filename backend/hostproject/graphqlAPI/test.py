from graphene_django.utils.testing import GraphQLTestCase
import json

from room.models.locations import Map, Country, Location, Next_to
from room.models.order import Unit, Turn, Order

class MyFancyTestCase(GraphQLTestCase):

     # setup test database to use throughout this class
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.map = Map.objects.create(name="A test map", max_countries=7)
        cls.countryA = Country.objects.create(name="country A", map=cls.map,colour='red')
        cls.locationA = Location.objects.create(name="location A",map=cls.map)
        cls.locationB = Location.objects.create(name="location B",map=cls.map)
        cls.nextToAB = Next_to.objects.create(location=cls.locationA, next_to=cls.locationB)
        cls.nextToBA = Next_to.objects.create(location=cls.locationB, next_to=cls.locationA)
        cls.unitA = Unit.objects.create(owner=cls.countryA,location=cls.locationA)
        cls.turn = Turn.objects.create(year=1994)
        cls.orderA = Order.objects.create(instruction='MVE', turn=cls.turn, target_unit=cls.unitA, current_location=cls.locationA, target_location=cls.locationB)


    def test_some_query(self):
        for tableName in ['turns', 'units', 'orders', 'locations']:
            querySyntax = "query{ " + tableName + " {id} }"
            response = self.query(querySyntax)
            content = json.loads(response.content)
            #print(content)

            # This validates the status code and if you get errors
            self.assertResponseNoErrors(response)
        