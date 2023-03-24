# Create your tests here.
from django.test import TestCase
from room.game.unit.abstract_unit import AbstractUnit
from room.game.unit.units import Army
from room.models.tables import Map,Country,Location,Next_to,Order,Outcome,Turn,Unit
from room.game.unit.unit_factory import UnitFactory

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

    def test_build(self):
        army = UnitFactory.build_unit(self.orderA)
        self.assertTrue(type(army) is Army)
        self.assertTrue(type(army.unit) is Unit)
        self.assertTrue(army.unit == self.unitA)
        self.assertFalse(army.can_float)
        self.assertTrue(type(army.unit.location) is Location)
        self.assertTrue(army.unit.location == self.locationA)
        self.assertTrue(type(army.unit.owner) is Country)
        self.assertTrue(army.unit.owner == self.countryA)


    #Each test takes self as a parameter
    def test_before_move(self):
        #self then relates to the database objects
        print(self.orderA)
        army = UnitFactory.build_unit(self.orderA)
        self.assertNotEqual(army.unit.location,self.orderA.target_location)


    #def test_abs(self):
        #abs = AbstractUnit(self.orderA)
        #self.assertEqual(abs.order, self.orderA)

    def test_move(self):
        army:AbstractUnit = UnitFactory.build_unit(self.orderA)
        before_location = army.unit.location 
        print('before_location')
        print(before_location)
        army.move()
        self.assertNotEqual(before_location, army.unit.location)