# Create your tests here.
from django.test import TestCase
from room.game.unitTypes import Unit
from room.game.legitamiseOrders import LegitamiseOrders
from room.game.resolveOrders import ResolveOrders
from room.models.locations import Country, Map, Location, Next_to
from room.models.order import MoveType, Order, Outcome, OutcomeType, Turn

# https://docs.djangoproject.com/en/4.1/topics/testing/tools/#django.test.TestCase 
class room_app_test_resolve_orders_simple_conflict(TestCase):
    # setup test database to use throughout this class
    @classmethod
    def setUpTestData(cls):
        cls.turn = Turn.objects.create(year=1994)
        cls.map = Map.objects.create(name="A test map", max_countries=7)

        # Locations
        cls.locationA = Location.objects.create(name="location A",map=cls.map)

        cls.locationB = Location.objects.create(name="location B",map=cls.map)
        cls.locationC = Location.objects.create(name="location C",map=cls.map)

        cls.locationD = Location.objects.create(name='location D',map=cls.map)
        cls.locationE = Location.objects.create(name='location E',map=cls.map)
        cls.locationF = Location.objects.create(name='location F',map=cls.map)

        cls.locationG = Location.objects.create(name='location G',map=cls.map,is_coast=True)
        cls.locationH = Location.objects.create(name='location H',map=cls.map,is_sea=True)
        cls.locationJ = Location.objects.create(name='location J',map=cls.map,is_coast=True)
        
        # Next To
        cls.nextToCB = Next_to.objects.create(location=cls.locationC, next_to=cls.locationB)
        cls.nextToBC = Next_to.objects.create(location=cls.locationB, next_to=cls.locationC)

        cls.nextToDE = Next_to.objects.create(location=cls.locationD, next_to=cls.locationE)
        cls.nextToED = Next_to.objects.create(location=cls.locationE, next_to=cls.locationD)
        cls.nextToFE = Next_to.objects.create(location=cls.locationF, next_to=cls.locationE)
        cls.nextToEF = Next_to.objects.create(location=cls.locationE, next_to=cls.locationF)
        cls.nextToFD = Next_to.objects.create(location=cls.locationF, next_to=cls.locationD)
        cls.nextToDF = Next_to.objects.create(location=cls.locationD, next_to=cls.locationF)

        cls.nextToGH = Next_to.objects.create(location=cls.locationG, next_to=cls.locationH)
        cls.nextToHG = Next_to.objects.create(location=cls.locationH, next_to=cls.locationG)
        cls.nextToHJ = Next_to.objects.create(location=cls.locationH, next_to=cls.locationJ)
        cls.nextToJH = Next_to.objects.create(location=cls.locationJ, next_to=cls.locationH)

        # Country
        cls.countryA = Country.objects.create(name="country A", map=cls.map,colour='red')
        cls.countryB = Country.objects.create(name="country B", map=cls.map,colour='blue')
        cls.countryC = Country.objects.create(name="country C", map=cls.map,colour='green')

    def test_check_two_locations_same_army(self):
        # A <- A
        unitA = Unit.objects.create(owner=self.countryA,location=self.locationB)
        unitB = Unit.objects.create(owner=self.countryA,location=self.locationC)
        order_1 = Order(instruction=MoveType.MOVE,turn=self.turn,
                                target_unit=unitA,current_location=self.locationB,
                                target_location=self.locationC)
        self.assertTrue(order_1.save())
        order_2 = Order(instruction=MoveType.HOLD,turn=self.turn,
                                target_unit=unitB,current_location=self.locationC)
        self.assertTrue(order_2.save())
        LegitamiseOrders(self.turn)
        ResolveOrders(self.turn)
        outcome_1 = Outcome.objects.get(order_reference=order_1)
        if type(outcome_1) is Outcome:
            self.assertEqual(outcome_1.validation, OutcomeType.BOUNCE)
        outcome_2 = Outcome.objects.get(order_reference=order_2)
        if type(outcome_2) is Outcome:
            self.assertEqual(outcome_2.validation, OutcomeType.MAYBE)
    
    def test_check_two_locations_different_army(self):
        # B <- A
        unitA = Unit.objects.create(owner=self.countryA,location=self.locationB)
        unitB = Unit.objects.create(owner=self.countryB,location=self.locationC)
        order_1 = Order(instruction=MoveType.MOVE,turn=self.turn,
                                target_unit=unitA,current_location=self.locationB,
                                target_location=self.locationC)
        self.assertTrue(order_1.save())
        order_2 = Order(instruction=MoveType.HOLD,turn=self.turn,
                                target_unit=unitB,current_location=self.locationC)
        self.assertTrue(order_2.save())
        LegitamiseOrders(self.turn)
        ResolveOrders(self.turn)
        outcome_1 = Outcome.objects.get(order_reference=order_1)
        if type(outcome_1) is Outcome:
            self.assertEqual(outcome_1.validation, OutcomeType.BOUNCE)
        outcome_2 = Outcome.objects.get(order_reference=order_2)
        if type(outcome_2) is Outcome:
            self.assertEqual(outcome_2.validation, OutcomeType.MAYBE)
    
    def test_check_two_locations_both_mve(self):
        # B <-> A
        unitA = Unit.objects.create(owner=self.countryA,location=self.locationB)
        unitB = Unit.objects.create(owner=self.countryB,location=self.locationC)
        order_1 = Order(instruction=MoveType.MOVE,turn=self.turn,
                                target_unit=unitA,current_location=self.locationB,
                                target_location=self.locationC)
        self.assertTrue(order_1.save())
        order_2 = Order(instruction=MoveType.MOVE,turn=self.turn,
                                target_unit=unitB,current_location=self.locationC,
                                target_location=self.locationB)
        self.assertTrue(order_2.save())
        LegitamiseOrders(self.turn)
        ResolveOrders(self.turn)
        outcome_1 = Outcome.objects.get(order_reference=order_1)
        if type(outcome_1) is Outcome:
            self.assertEqual(outcome_1.validation, OutcomeType.BOUNCE)
        outcome_2 = Outcome.objects.get(order_reference=order_2)
        if type(outcome_2) is Outcome:
            self.assertEqual(outcome_2.validation, OutcomeType.BOUNCE)

    def test_check_three_locations_both_mve_to_location_unoccupied(self):
        # D -> E
        # F -> E
        unitA = Unit.objects.create(owner=self.countryA,location=self.locationD)
        unitB = Unit.objects.create(owner=self.countryB,location=self.locationF)
        order_1 = Order(instruction=MoveType.MOVE,turn=self.turn,
                                target_unit=unitA,current_location=self.locationD,
                                target_location=self.locationE)
        self.assertTrue(order_1.save())
        order_2 = Order(instruction=MoveType.MOVE,turn=self.turn,
                                target_unit=unitB,current_location=self.locationF,
                                target_location=self.locationE)
        self.assertTrue(order_2.save())
        LegitamiseOrders(self.turn)
        #print(Outcome.objects.grab_mve_attacking_orders(self.locationE,self.turn))
        #print(Outcome.objects.grab_highest_attacking_mve(self.locationE,self.turn))
        ResolveOrders(self.turn)
        outcome_1 = Outcome.objects.get(order_reference=order_1)
        if type(outcome_1) is Outcome:
            self.assertEqual(outcome_1.validation, OutcomeType.BOUNCE)
        outcome_2 = Outcome.objects.get(order_reference=order_2)
        if type(outcome_2) is Outcome:
            self.assertEqual(outcome_2.validation, OutcomeType.BOUNCE)

    def test_check_three_locations_both_mve_to_location_occupied(self):
        # D -> E
        # F -> E
        # E Hold
        unitA = Unit.objects.create(owner=self.countryA,location=self.locationD)
        unitB = Unit.objects.create(owner=self.countryB,location=self.locationF)
        unitC = Unit.objects.create(owner=self.countryC,location=self.locationE)
        order_1 = Order(instruction=MoveType.MOVE,turn=self.turn,
                                target_unit=unitA,current_location=self.locationD,
                                target_location=self.locationE)
        self.assertTrue(order_1.save())
        order_2 = Order(instruction=MoveType.MOVE,turn=self.turn,
                                target_unit=unitB,current_location=self.locationF,
                                target_location=self.locationE)
        self.assertTrue(order_2.save())
        order_3 = Order(instruction=MoveType.HOLD,turn=self.turn,
                                target_unit=unitC,current_location=self.locationE)
        self.assertTrue(order_3.save())
        LegitamiseOrders(self.turn)
        ResolveOrders(self.turn)
        outcome_1 = Outcome.objects.get(order_reference=order_1)
        if type(outcome_1) is Outcome:
            self.assertEqual(outcome_1.validation, OutcomeType.BOUNCE)
        outcome_2 = Outcome.objects.get(order_reference=order_2)
        if type(outcome_2) is Outcome:
            self.assertEqual(outcome_2.validation, OutcomeType.BOUNCE)
        outcome_3 = Outcome.objects.get(order_reference=order_3)
        if type(outcome_3) is Outcome:
            self.assertEqual(outcome_3.validation, OutcomeType.MAYBE)

    def test_check_three_locations_mve_and_spt_to_location_occupied(self):
        # D -> E
        # F spt D -> E
        unitA = Unit.objects.create(owner=self.countryA,location=self.locationD)
        unitB = Unit.objects.create(owner=self.countryB,location=self.locationF)
        unitC = Unit.objects.create(owner=self.countryC,location=self.locationE)
        order_1 = Order(instruction=MoveType.MOVE,turn=self.turn,
                                target_unit=unitA,current_location=self.locationD,
                                target_location=self.locationE)
        self.assertTrue(order_1.save())
        order_2 = Order(instruction=MoveType.SUPPORT,turn=self.turn,
                                target_unit=unitB,current_location=self.locationF,
                                reference_unit=unitA,
                                reference_unit_current_location=self.locationD,
                                reference_unit_new_location=self.locationE)
        self.assertTrue(order_2.save())
        order_3 = Order(instruction=MoveType.HOLD,turn=self.turn,
                                target_unit=unitC,current_location=self.locationE)
        self.assertTrue(order_3.save())
        LegitamiseOrders(self.turn)
        ResolveOrders(self.turn)
        outcome_1 = Outcome.objects.get(order_reference=order_1)
        if type(outcome_1) is Outcome:
            self.assertEqual(outcome_1.validation, OutcomeType.MAYBE)
        outcome_2 = Outcome.objects.get(order_reference=order_2)
        if type(outcome_2) is Outcome:
            self.assertEqual(outcome_2.validation, OutcomeType.VOID)
        outcome_3 = Outcome.objects.get(order_reference=order_3)
        if type(outcome_3) is Outcome:
            self.assertEqual(outcome_3.validation, OutcomeType.DISLODGED)

    def test_check_three_locations_all_mve_clockwise(self):
        # D -> E
        # F -> D
        # E -> F
        unitA = Unit.objects.create(owner=self.countryA,location=self.locationD)
        unitB = Unit.objects.create(owner=self.countryB,location=self.locationF)
        unitC = Unit.objects.create(owner=self.countryC,location=self.locationE)
        order_1 = Order(instruction=MoveType.MOVE,turn=self.turn,
                                target_unit=unitA,current_location=self.locationD,
                                target_location=self.locationE)
        self.assertTrue(order_1.save())
        order_2 = Order(instruction=MoveType.MOVE,turn=self.turn,
                                target_unit=unitB,current_location=self.locationF,
                                target_location=self.locationD)
        self.assertTrue(order_2.save())
        order_3 = Order(instruction=MoveType.MOVE,turn=self.turn,
                                target_unit=unitC,current_location=self.locationE,
                                target_location=self.locationF)
        self.assertTrue(order_3.save())
        LegitamiseOrders(self.turn)
        ResolveOrders(self.turn)
        outcome_1 = Outcome.objects.get(order_reference=order_1)
        if type(outcome_1) is Outcome:
            self.assertEqual(outcome_1.validation, OutcomeType.MAYBE)
        outcome_2 = Outcome.objects.get(order_reference=order_2)
        if type(outcome_2) is Outcome:
            self.assertEqual(outcome_2.validation, OutcomeType.MAYBE)
        outcome_3 = Outcome.objects.get(order_reference=order_3)
        if type(outcome_3) is Outcome:
            self.assertEqual(outcome_3.validation, OutcomeType.MAYBE)

    def test_check_three_locations_chain_bounce(self):
        # D -> E - bounce
        # E -> F - bounce
        # F Hold - maybe
        unitA = Unit.objects.create(owner=self.countryA,location=self.locationD)
        unitB = Unit.objects.create(owner=self.countryB,location=self.locationE)
        unitC = Unit.objects.create(owner=self.countryC,location=self.locationF)
        order_1 = Order(instruction=MoveType.MOVE,turn=self.turn,
                                target_unit=unitA,current_location=self.locationD,
                                target_location=self.locationE)
        self.assertTrue(order_1.save())
        order_2 = Order(instruction=MoveType.MOVE,turn=self.turn,
                                target_unit=unitB,current_location=self.locationE,
                                target_location=self.locationF)
        self.assertTrue(order_2.save())
        order_3 = Order(instruction=MoveType.HOLD,turn=self.turn,
                                target_unit=unitC,current_location=self.locationF)
        self.assertTrue(order_3.save())
        LegitamiseOrders(self.turn)
        ResolveOrders(self.turn)
        outcome_1 = Outcome.objects.get(order_reference=order_1)
        if type(outcome_1) is Outcome:
            self.assertEqual(outcome_1.validation, OutcomeType.BOUNCE)
        outcome_2 = Outcome.objects.get(order_reference=order_2)
        if type(outcome_2) is Outcome:
            self.assertEqual(outcome_2.validation, OutcomeType.BOUNCE)
        outcome_3 = Outcome.objects.get(order_reference=order_3)
        if type(outcome_3) is Outcome:
            self.assertEqual(outcome_3.validation, OutcomeType.MAYBE)

    def test_check_three_locations_invalid_cut_support(self):
        # D -> E - maybe
        # F SPT D -> E - maybe
        # E -> F - void/bounce
        unitA = Unit.objects.create(owner=self.countryA,location=self.locationD)
        unitB = Unit.objects.create(owner=self.countryB,location=self.locationF)
        unitC = Unit.objects.create(owner=self.countryC,location=self.locationE)
        order_1 = Order(instruction=MoveType.MOVE,turn=self.turn,
                                target_unit=unitA,current_location=self.locationD,
                                target_location=self.locationE)
        self.assertTrue(order_1.save())
        order_2 = Order(instruction=MoveType.SUPPORT,turn=self.turn,
                                target_unit=unitB,current_location=self.locationF,
                                reference_unit=unitA,
                                reference_unit_current_location=self.locationD,
                                reference_unit_new_location=self.locationE)
        self.assertTrue(order_2.save())
        order_3 = Order(instruction=MoveType.MOVE,turn=self.turn,
                                target_unit=unitC,current_location=self.locationE,
                                target_location=self.locationF)
        self.assertTrue(order_3.save())
        LegitamiseOrders(self.turn)
        ResolveOrders(self.turn)
        outcome_1 = Outcome.objects.get(order_reference=order_1)
        if type(outcome_1) is Outcome:
            self.assertEqual(outcome_1.validation, OutcomeType.MAYBE)
        outcome_2 = Outcome.objects.get(order_reference=order_2)
        if type(outcome_2) is Outcome:
            self.assertEqual(outcome_2.validation, OutcomeType.MAYBE)
        outcome_3 = Outcome.objects.get(order_reference=order_3)
        if type(outcome_3) is Outcome:
            self.assertEqual(outcome_3.validation, OutcomeType.BOUNCE)

    def test_check_three_locations_cvy_bounce(self):
        # D -> E - bounce
        # E -> F - bounce
        # F Hold - maybe
        unitA = Unit.objects.create(owner=self.countryA,location=self.locationG)
        unitB = Unit.objects.create(owner=self.countryB,location=self.locationH,can_float=True)
        unitC = Unit.objects.create(owner=self.countryC,location=self.locationJ)
        order_1 = Order(instruction=MoveType.MOVE,turn=self.turn,
                                target_unit=unitA,current_location=self.locationG,
                                target_location=self.locationJ)
        self.assertTrue(order_1.save())
        order_2 = Order(instruction=MoveType.CONVOY,turn=self.turn,
                                target_unit=unitB,current_location=self.locationH,
                                reference_unit=unitA,
                                reference_unit_current_location=self.locationG,
                                reference_unit_new_location=self.locationJ)
        self.assertTrue(order_2.save())
        order_3 = Order(instruction=MoveType.HOLD,turn=self.turn,
                                target_unit=unitC,current_location=self.locationJ)
        self.assertTrue(order_3.save())
        LegitamiseOrders(self.turn)
        ResolveOrders(self.turn)
        outcome_1 = Outcome.objects.get(order_reference=order_1)
        if type(outcome_1) is Outcome:
            self.assertEqual(outcome_1.validation, OutcomeType.BOUNCE)
        outcome_2 = Outcome.objects.get(order_reference=order_2)
        if type(outcome_2) is Outcome:
            self.assertEqual(outcome_2.validation, OutcomeType.MAYBE)
        outcome_3 = Outcome.objects.get(order_reference=order_3)
        if type(outcome_3) is Outcome:
            self.assertEqual(outcome_3.validation, OutcomeType.MAYBE)

    def test_spt_diagram_24(self):
        # D -> F - bounce
        # E SPT D -> F - void
        # F hold - maybe
        unitA = Unit.objects.create(owner=self.countryA,location=self.locationD)
        unitB = Unit.objects.create(owner=self.countryB,location=self.locationE)
        unitC = Unit.objects.create(owner=self.countryB,location=self.locationF)

        order_3 = Order(instruction=MoveType.HOLD,turn=self.turn,
                                target_unit=unitC,current_location=self.locationF)
        self.assertTrue(order_3.save())
        order_1 = Order(instruction=MoveType.MOVE,turn=self.turn,
                                target_unit=unitA,current_location=self.locationD,
                                target_location=self.locationF)
        self.assertTrue(order_1.save())
        order_2 = Order(instruction=MoveType.SUPPORT,turn=self.turn,
                                target_unit=unitB,current_location=self.locationE,
                                reference_unit=unitA,
                                reference_unit_current_location=self.locationD,
                                reference_unit_new_location=self.locationF)
        self.assertTrue(order_2.save())
        
        LegitamiseOrders(self.turn)
        #print('spt',Outcome.objects.grab_related_spt_orders(order_1,self.turn).first().validation)
        ResolveOrders(self.turn)
        outcome_1 = Outcome.objects.get(order_reference=order_1)
        if type(outcome_1) is Outcome:
            self.assertEqual(outcome_1.validation, OutcomeType.BOUNCE)
        outcome_2 = Outcome.objects.get(order_reference=order_2)
        if type(outcome_2) is Outcome:
            self.assertEqual(outcome_2.validation, OutcomeType.VOID)
        outcome_3 = Outcome.objects.get(order_reference=order_3)
        if type(outcome_3) is Outcome:
            self.assertEqual(outcome_3.validation, OutcomeType.MAYBE)