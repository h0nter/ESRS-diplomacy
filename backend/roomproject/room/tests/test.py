# Create your tests here.
from django.test import TestCase
from room.models.unit import Unit
from room.models.locations import Map,Country,Location,Next_to
from room.models.order import Order
from room.models.turn import Turn
from room.models.room import Room

# https://docs.djangoproject.com/en/4.1/topics/testing/tools/#django.test.TestCase 
class room_app_unitTest1(TestCase):
    # setup test database to use throughout this class
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.map = Map.objects.create(name="A test map", max_countries=7)
        cls.countryA = Country.objects.create(name="country A", map=cls.map,colour='red')
        cls.locationA = Location.objects.create(name="location A",map=cls.map)
        cls.locationB = Location.objects.create(name="location B",map=cls.map, is_coast=True)
        cls.locationC = Location.objects.create(name='location C',map=cls.map,is_coast=True)
        cls.locationD = Location.objects.create(name='location D',map=cls.map,is_coast=True)
        cls.locationE = Location.objects.create(name='location E',map=cls.map,is_sea=True)
        cls.nextToAB = Next_to.objects.create(location=cls.locationA, next_to=cls.locationB)
        cls.nextToBA = Next_to.objects.create(location=cls.locationB, next_to=cls.locationA)
        cls.nextToCB = Next_to.objects.create(location=cls.locationC, next_to=cls.locationB)
        cls.nextToBC = Next_to.objects.create(location=cls.locationB, next_to=cls.locationC)
        cls.nextToAD = Next_to.objects.create(location=cls.locationA, next_to=cls.locationD)
        cls.nextToDA = Next_to.objects.create(location=cls.locationD, next_to=cls.locationA)
        cls.nextToBE = Next_to.objects.create(location=cls.locationB, next_to=cls.locationE)
        cls.nextToEB = Next_to.objects.create(location=cls.locationE, next_to=cls.locationB)
        cls.nextToDE = Next_to.objects.create(location=cls.locationD, next_to=cls.locationE)
        cls.nextToED = Next_to.objects.create(location=cls.locationE, next_to=cls.locationD)
        cls.unitA = Unit.objects.create(owner=cls.countryA,location=cls.locationA)
        cls.unitB = Unit.objects.create(owner=cls.countryA,location=cls.locationC)
        cls.unitC = Unit.objects.create(owner=cls.countryA,location=cls.locationB)
        cls.unitD = Unit.objects.create(owner=cls.countryA,location=cls.locationE,can_float=True)
        cls.turn = Turn.objects.create(year=1994)
        cls.room = Room.objects.create(current_turn=cls.turn,room_name='test Room')
        cls.orderMVEValid = Order.objects.create(instruction='MVE', turn=cls.turn, room=cls.room, unit=cls.unitA, current_location=cls.locationA, target_location=cls.locationB)
        cls.orderMVEInvalid = Order.objects.create(instruction='MVE', turn=cls.turn, room=cls.room, unit=cls.unitA, current_location=cls.locationA, target_location=cls.locationC)
        cls.orderSPTValid = Order.objects.create(instruction='SPT', turn=cls.turn, room=cls.room, unit=cls.unitB, current_location=cls.locationC, reference_unit=cls.unitA,\
                                                  reference_unit_current_location=cls.locationA, reference_unit_new_location=cls.locationB)
        cls.orderSPTInvalid = Order.objects.create(instruction='SPT', turn=cls.turn, room=cls.room, unit=cls.unitB, current_location=cls.locationC, reference_unit=cls.unitA,\
                                                  reference_unit_current_location=cls.locationA, reference_unit_new_location=cls.locationD)
        cls.orderMVECVYValid = Order.objects.create(instruction='MVE', turn=cls.turn, room=cls.room, unit=cls.unitC, current_location=cls.locationB, target_location=cls.locationD)
        cls.orderCVYValid = Order.objects.create(instruction='CVY', turn=cls.turn, room=cls.room, unit=cls.unitD, current_location=cls.locationE, reference_unit=cls.unitC,\
                                                  reference_unit_current_location=cls.locationB, reference_unit_new_location=cls.locationD)    
        

    def test_build(self):
        army = self.orderMVEValid.unit
        self.assertTrue(type(army) is Unit)
        self.assertTrue(army == self.unitA)
        self.assertFalse(army.can_float)
        self.assertTrue(type(army.location) is Location)
        self.assertTrue(army.location == self.locationA)
        self.assertTrue(type(army.owner) is Country)
        self.assertTrue(army.owner == self.countryA)
