# Create your tests here.
from django.test import TestCase
from backend.room.game.unit.units import Army
from backend.room.models.tables import Map,Country,Location,Next_to,Order,Outcome,Turn,Unit
from backend.room.game.unit.unit_factory import UnitFactory

# https://docs.djangoproject.com/en/4.1/topics/testing/tools/#django.test.TestCase 
class room_app_unitTest1(TestCase):
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

    # def test_insert(self):
    #     from .initial_insert import InitialInsert as II
    #     II.all_insert()

    def test_build(self):
        army = UnitFactory.build_unit(self.orderA)
        self.assertTrue(army is Army)

    #Each test takes self as a parameter
    def test_before_move(self):
        #self then relates to the database objects
        print(self.orderA)
        army = UnitFactory.build_unit(self.orderA)
        self.assertNotEqual(army.location,self.orderA.target_location)
        # army = UnitFactory.build_unit(self.orderA)
        # army.move()
        # self.assertEqual(army.location, self.orderA.target_location)