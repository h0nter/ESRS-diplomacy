# Create your tests here.
from django.test import TestCase
from room.game.unitTypes import Unit
from room.models.locations import Map,Country,Location,Next_to
from room.models.order import Order,Outcome,Turn,OutcomeType,MoveType

# https://docs.djangoproject.com/en/4.1/topics/testing/tools/#django.test.TestCase 
class room_app_test_legitamise_orders(TestCase):
    # setup test database to use throughout this class
    @classmethod
    def setUpTestData(cls):
        cls.turn = Turn.objects.create(year=1994)
        cls.map = Map.objects.create(name="A test map", max_countries=7)
        cls.countryA = Country.objects.create(name="country A", map=cls.map,colour='red')
        cls.locationA = Location.objects.create(name="location A",map=cls.map)
        cls.locationB = Location.objects.create(name="location B",map=cls.map, is_coast=True)
        cls.locationC = Location.objects.create(name='location C',map=cls.map,is_coast=True,is_sea=True)
        cls.nextToAB = Next_to.objects.create(location=cls.locationA, next_to=cls.locationB)
        cls.nextToBA = Next_to.objects.create(location=cls.locationB, next_to=cls.locationA)
        cls.nextToCB = Next_to.objects.create(location=cls.locationC, next_to=cls.locationB)
        cls.nextToBC = Next_to.objects.create(location=cls.locationB, next_to=cls.locationC)
        cls.unitA = Unit.objects.create(owner=cls.countryA,location=cls.locationA)        
        cls.unitB = Unit.objects.create(owner=cls.countryA,location=cls.locationC)
        cls.unitC = Unit.objects.create(owner=cls.countryA,location=cls.locationB,can_float=True)

        

    def test_valid_hold(self):
        hold = Order.objects.create(instruction=MoveType.HOLD,turn=self.turn,
                                    target_unit=self.unitA,current_location=self.locationA)
        self.assertTrue(hold.save())


    def test_invalid_hold(self):
        try:
            hold = Order.objects.create(instruction=MoveType.HOLD,turn=self.turn,
                                     target_unit=self.unitA,current_location='locationA')
        except Exception as e:
            self.assertRaisesMessage(ValueError,str(e))
    
    def test_valid_mve(self):
        mve = Order.objects.create(instruction=MoveType.MOVE,turn=self.turn,
                                    target_unit=self.unitA,
                                    current_location=self.locationA,
                                    target_location=self.locationB)
        self.assertTrue(mve.save())

    def test_invalid_mve(self):
        try:
            mve = Order.objects.create(instruction=MoveType.MOVE,turn=self.turn,
                                    target_unit=self.unitA,
                                    current_location=self.locationA,
                                    target_location='locationB')
        except Exception as e:
            self.assertRaisesMessage(ValueError,str(e))

    def test_valid_spt(self):
        spt = Order.objects.create(instruction=MoveType.SUPPORT,turn=self.turn,
                                    target_unit=self.unitB,
                                    current_location=self.locationC,
                                    reference_unit=self.unitA,
                                    reference_unit_current_location=self.locationA,
                                    reference_unit_new_location=self.locationB)
        self.assertTrue(spt.save())

    def test_invalid_spt(self):
        spt = Order.objects.create(instruction=MoveType.SUPPORT,turn=self.turn,
                                    target_unit=self.unitB,
                                    current_location=self.locationC,
                                    reference_unit=self.unitA)
        self.assertFalse(spt.save())

    def test_valid_cvy(self):
        cvy = Order.objects.create(instruction=MoveType.CONVOY,turn=self.turn,
                                    target_unit=self.unitC,
                                    current_location=self.locationC,
                                    reference_unit=self.unitA,
                                    reference_unit_current_location=self.locationA,
                                    reference_unit_new_location=self.locationB)
        print('unitAfloat {}'.format(self.unitA.can_float))
        print('unitCfloat {}'.format(self.unitC.can_float))
        print('target_location {}'.format(cvy.target_location))
        print('can_float {}'.format(cvy.target_unit.can_float))
        print('is_sea {}'.format(cvy.current_location.is_sea))
        print('save {}'.format(cvy.save()))
        self.assertTrue(cvy.save())

    def test_invalid_cvy(self):
        cvy = Order.objects.create(instruction=MoveType.CONVOY,turn=self.turn,
                                    target_unit=self.unitB,
                                    current_location=self.locationC,
                                    reference_unit=self.unitA)
        self.assertFalse(cvy.save())