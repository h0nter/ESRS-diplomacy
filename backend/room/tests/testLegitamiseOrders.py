# Create your tests here.
from django.test import TestCase
from room.game.legitamiseOrders import LegitamiseOrders
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
        cls.locationB = Location.objects.create(name="location B",map=cls.map, is_coast=True,is_sea=True)
        cls.locationC = Location.objects.create(name='location C',map=cls.map,is_coast=True,is_sea=True)
        cls.locationD = Location.objects.create(name='location D',map=cls.map,is_coast=True,is_sea=True)
        cls.locationE = Location.objects.create(name='location E',map=cls.map,is_sea=True)
        cls.nextToAB = Next_to.objects.create(location=cls.locationA, next_to=cls.locationB)
        cls.nextToBA = Next_to.objects.create(location=cls.locationB, next_to=cls.locationA)
        cls.nextToCB = Next_to.objects.create(location=cls.locationC, next_to=cls.locationB)
        cls.nextToBC = Next_to.objects.create(location=cls.locationB, next_to=cls.locationC)
        cls.nextToCA = Next_to.objects.create(location=cls.locationC, next_to=cls.locationA)
        cls.nextToAC = Next_to.objects.create(location=cls.locationA, next_to=cls.locationC)
        cls.nextToCD = Next_to.objects.create(location=cls.locationC, next_to=cls.locationD)
        cls.nextToDC = Next_to.objects.create(location=cls.locationD, next_to=cls.locationC)
        cls.nextToED = Next_to.objects.create(location=cls.locationE, next_to=cls.locationD)
        cls.nextToDE = Next_to.objects.create(location=cls.locationD, next_to=cls.locationE)
        cls.unitA = Unit.objects.create(owner=cls.countryA,location=cls.locationA)        
        cls.unitB = Unit.objects.create(owner=cls.countryA,location=cls.locationC)
        cls.unitC = Unit.objects.create(owner=cls.countryA,location=cls.locationB,can_float=True)
        cls.unitD = Unit.objects.create(owner=cls.countryA,location=cls.locationD)
        cls.unitE = Unit.objects.create(owner=cls.countryA,location=cls.locationE)

        

    def test_valid_hold(self):
        hold = Order(instruction=MoveType.HOLD,turn=self.turn,
                                    target_unit=self.unitA,current_location=self.locationA)
        self.assertTrue(hold.save())


    def test_invalid_hold(self):
        try:
            hold = Order(instruction=MoveType.HOLD,turn=self.turn,
                                     target_unit=self.unitA,current_location='locationA')
        except Exception as e:
            self.assertRaisesMessage(ValueError,str(e))

    def test_invalid_hold2(self):
        hold = Order(instruction=MoveType.HOLD,turn=self.turn,
                                     target_unit=self.unitA,current_location=self.locationE)
        self.assertFalse(hold.save())

    def test_invalid_hold3(self):
        hold = Order(instruction=MoveType.HOLD,turn=self.turn,
                                     target_unit=self.unitE,current_location=self.locationE)
        self.assertFalse(hold.save())
    
    def test_valid_mve(self):
        mve = Order(instruction=MoveType.MOVE,turn=self.turn,
                                    target_unit=self.unitA,
                                    current_location=self.locationA,
                                    target_location=self.locationB)
        self.assertTrue(mve.save())

    def test_invalid_mve(self):
        try:
            mve = Order(instruction=MoveType.MOVE,turn=self.turn,
                                    target_unit=self.unitA,
                                    current_location=self.locationA,
                                    target_location='locationB')
        except Exception as e:
            self.assertRaisesMessage(ValueError,str(e))

    def test_invalid_mve2(self):
        mve = Order(instruction=MoveType.MOVE,turn=self.turn,
                                    target_unit=self.unitD,
                                    current_location=self.locationD,
                                    target_location=self.locationE)
        self.assertFalse(mve.save())

    def test_valid_spt(self):
        spt = Order(instruction=MoveType.SUPPORT,turn=self.turn,
                                    target_unit=self.unitB,
                                    current_location=self.locationC,
                                    reference_unit=self.unitA,
                                    reference_unit_current_location=self.locationA,
                                    reference_unit_new_location=self.locationB)
        self.assertTrue(spt.save())

    def test_invalid_spt(self):
        spt = Order(instruction=MoveType.SUPPORT,turn=self.turn,
                                    target_unit=self.unitB,
                                    current_location=self.locationC,
                                    reference_unit=self.unitA)
        self.assertFalse(spt.save())

    def test_valid_cvy(self):
        cvy = Order(instruction=MoveType.CONVOY,turn=self.turn,
                                    target_unit=self.unitC,
                                    current_location=self.locationB,
                                    reference_unit=self.unitA,
                                    reference_unit_current_location=self.locationA,
                                    reference_unit_new_location=self.locationC)
        self.assertTrue(cvy.save())

    def test_invalid_cvy(self):
        cvy = Order(instruction=MoveType.CONVOY,turn=self.turn,
                                    target_unit=self.unitB,
                                    current_location=self.locationC,
                                    reference_unit=self.unitA)
        self.assertFalse(cvy.save())

    def test_legit_orders(self):
        # create orders
        mve = Order(instruction=MoveType.MOVE,turn=self.turn,
                                    target_unit=self.unitA,
                                    current_location=self.locationA,
                                    target_location=self.locationB)
        self.assertTrue(mve.save())
        hold = Order(instruction=MoveType.HOLD,turn=self.turn,
                                    target_unit=self.unitA,current_location=self.locationA)
        self.assertTrue(hold.save())
        spt = Order(instruction=MoveType.SUPPORT,turn=self.turn,
                                    target_unit=self.unitB,
                                    current_location=self.locationC,
                                    reference_unit=self.unitA,
                                    reference_unit_current_location=self.locationA,
                                    reference_unit_new_location=self.locationB)
        self.assertTrue(spt.save())
        spt2 = Order(instruction=MoveType.SUPPORT,turn=self.turn,
                                    target_unit=self.unitD,
                                    current_location=self.locationD,
                                    reference_unit=self.unitA,
                                    reference_unit_current_location=self.locationA,
                                    reference_unit_new_location=self.locationC)
        self.assertTrue(spt2.save())
        cvy = Order(instruction=MoveType.CONVOY,turn=self.turn,
                                    target_unit=self.unitC,
                                    current_location=self.locationB,
                                    reference_unit=self.unitA,
                                    reference_unit_current_location=self.locationA,
                                    reference_unit_new_location=self.locationC)
        self.assertTrue(cvy.save())
        cvy2 = Order(instruction=MoveType.CONVOY,turn=self.turn,
                                    target_unit=self.unitC,
                                    current_location=self.locationB,
                                    reference_unit=self.unitA,
                                    reference_unit_current_location=self.locationA,
                                    reference_unit_new_location=self.locationB)
        self.assertTrue(cvy2.save())
        # legitamise them
        LegitamiseOrders(self.turn)
        # check outcomes
        mve_outcome = Outcome.objects.filter(order_reference=mve).first()
        self.assertIsInstance(mve_outcome,Outcome)
        if type(mve_outcome) is Outcome:
            self.assertEqual(mve_outcome.validation, OutcomeType.MAYBE)

        hold_outcome = Outcome.objects.filter(order_reference=hold).first()
        self.assertIsInstance(hold_outcome,Outcome)
        if type(hold_outcome) is Outcome:
            self.assertEqual(hold_outcome.validation, OutcomeType.MAYBE)

        spt_outcome = Outcome.objects.filter(order_reference=spt).first()
        self.assertIsInstance(spt_outcome,Outcome)
        if type(spt_outcome) is Outcome:
            self.assertEqual(spt_outcome.validation, OutcomeType.MAYBE)

        spt2_outcome = Outcome.objects.filter(order_reference=spt2).first()
        self.assertIsInstance(spt2_outcome,Outcome)
        if type(spt2_outcome) is Outcome:
            self.assertEqual(spt2_outcome.validation, OutcomeType.VOID)

        spt_outcome = Outcome.objects.filter(order_reference=spt).first()
        self.assertIsInstance(spt_outcome,Outcome)
        if type(spt_outcome) is Outcome:
            self.assertEqual(spt_outcome.validation, OutcomeType.MAYBE)

        cvy_outcome = Outcome.objects.filter(order_reference=cvy).first()
        self.assertIsInstance(cvy_outcome,Outcome)
        if type(cvy_outcome) is Outcome:
            self.assertEqual(cvy_outcome.validation, OutcomeType.VOID)

        cvy2_outcome = Outcome.objects.filter(order_reference=cvy2).first()
        self.assertIsInstance(cvy2_outcome,Outcome)
        if type(cvy2_outcome) is Outcome:
            self.assertEqual(cvy2_outcome.validation, OutcomeType.MAYBE)
        

        