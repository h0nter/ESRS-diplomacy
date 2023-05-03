# Create your tests here.
from django.test import TestCase
from room.game.unitTypes import Unit
# from room.game.unit.abstract_unit import AbstractUnit
from room.models.locations import Map,Country,Location,Next_to
from room.models.order import Order,Outcome,Turn

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
        cls.orderMVEValid = Order.objects.create(instruction='MVE', turn=cls.turn, target_unit=cls.unitA, current_location=cls.locationA, target_location=cls.locationB)
        cls.orderMVEInvalid = Order.objects.create(instruction='MVE', turn=cls.turn, target_unit=cls.unitA, current_location=cls.locationA, target_location=cls.locationC)
        cls.orderSPTValid = Order.objects.create(instruction='SPT', turn=cls.turn, target_unit=cls.unitB, current_location=cls.locationC, reference_unit=cls.unitA,\
                                                  reference_unit_current_location=cls.locationA, reference_unit_new_location=cls.locationB)
        cls.orderSPTInvalid = Order.objects.create(instruction='SPT', turn=cls.turn, target_unit=cls.unitB, current_location=cls.locationC, reference_unit=cls.unitA,\
                                                  reference_unit_current_location=cls.locationA, reference_unit_new_location=cls.locationD)
        cls.orderMVECVYValid = Order.objects.create(instruction='MVE', turn=cls.turn, target_unit=cls.unitC, current_location=cls.locationB, target_location=cls.locationD)
        cls.orderCVYValid = Order.objects.create(instruction='CVY', turn=cls.turn, target_unit=cls.unitD, current_location=cls.locationE, reference_unit=cls.unitC,\
                                                  reference_unit_current_location=cls.locationB, reference_unit_new_location=cls.locationD)    
        

    def test_build(self):
        army = self.orderMVEValid.target_unit
        self.assertTrue(type(army) is Unit)
        self.assertTrue(army == self.unitA)
        self.assertFalse(army.can_float)
        self.assertTrue(type(army.location) is Location)
        self.assertTrue(army.location == self.locationA)
        self.assertTrue(type(army.owner) is Country)
        self.assertTrue(army.owner == self.countryA)


    #Each test takes self as a parameter
    def test_before_move(self):
        #self then relates to the database objects
        army = self.orderMVEValid.target_unit
        self.assertNotEqual(army.location,self.orderMVEValid.target_location)


    #def test_abs(self):
        #abs = AbstractUnit(self.orderA)
        #self.assertEqual(abs.order, self.orderA)

    def test_valid_move(self):
        unit:Unit = self.orderMVEValid.target_unit
        self.assertEqual(self.orderMVEValid.instruction,'MVE')
        self.assertTrue(unit.validate_move(self.orderMVEValid))
        

    def test_move(self):
        army = self.orderMVEValid.target_unit
        before_location = army.location 
        army.move(self.orderMVEValid.target_location)
        self.assertNotEqual(before_location,army.location)
        self.assertNotEqual(self.locationA,self.unitA.location)

    def test_invalid_move(self):
        unit:Unit = self.orderMVEInvalid.target_unit
        self.assertEqual(self.orderMVEInvalid.instruction,'MVE')
        self.assertFalse(unit.validate_move(self.orderMVEInvalid))

    def test_valid_support(self):
        unit:Unit = self.orderSPTValid.target_unit
        self.assertEqual(self.orderSPTValid.instruction,'SPT')
        self.assertTrue(unit.validate_support(self.orderSPTValid,self.turn))

    def test_invalid_support(self):
        unit:Unit = self.orderSPTInvalid.target_unit
        self.assertEqual(self.orderSPTInvalid.instruction,'SPT')
        self.assertFalse(unit.validate_support(self.orderSPTInvalid,self.turn))

    def test_convoy_move(self):
        army:Unit = self.orderMVECVYValid.target_unit
        self.assertEqual(self.orderMVECVYValid.instruction,'MVE')
        self.assertTrue(army.validate_move(self.orderMVECVYValid))
        fleet:Unit = self.orderCVYValid.target_unit
        self.assertEqual(self.orderCVYValid.instruction,'CVY')
        self.assertTrue(fleet.validate_convoy(self.orderCVYValid,self.turn))