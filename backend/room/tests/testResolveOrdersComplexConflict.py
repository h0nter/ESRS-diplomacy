# Create your tests here.
from django.test import TestCase
from room.game.unitTypes import Unit
from room.game.legitamiseOrders import LegitamiseOrders
from room.game.resolveOrders import ResolveOrders
from room.models.locations import Country, Map, Location, Next_to
from room.models.order import MoveType, Order, Outcome, OutcomeType, Turn

# https://docs.djangoproject.com/en/4.1/topics/testing/tools/#django.test.TestCase 
class room_app_test_resolve_orders_complex_conflict(TestCase):
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

        cls.locationTun = Location.objects.create(name='location Tun',map=cls.map,is_coast=True)
        cls.locationTyn = Location.objects.create(name='location Tyn',map=cls.map,is_sea=True)
        cls.locationRom = Location.objects.create(name='location Rom',map=cls.map,is_coast=True)
        cls.locationNap = Location.objects.create(name='location Nap',map=cls.map,is_coast=True)
        cls.locationIon = Location.objects.create(name='location Ion',map=cls.map,is_sea=True)
        cls.locationApu = Location.objects.create(name='location Ion',map=cls.map,is_coast=True)

        # Next To
        cls.nextToCB = Next_to.objects.create(location=cls.locationC, next_to=cls.locationB)
        cls.nextToBC = Next_to.objects.create(location=cls.locationB, next_to=cls.locationC)

        cls.nextToDE = Next_to.objects.create(location=cls.locationD, next_to=cls.locationE)
        cls.nextToED = Next_to.objects.create(location=cls.locationE, next_to=cls.locationD)
        cls.nextToFE = Next_to.objects.create(location=cls.locationF, next_to=cls.locationE)
        cls.nextToEF = Next_to.objects.create(location=cls.locationE, next_to=cls.locationF)
        cls.nextToFD = Next_to.objects.create(location=cls.locationF, next_to=cls.locationD)
        cls.nextToDF = Next_to.objects.create(location=cls.locationD, next_to=cls.locationF)

        cls.nextToTunTyn = Next_to.objects.create(location=cls.locationTun, next_to=cls.locationTyn)
        cls.nextToTynTun = Next_to.objects.create(location=cls.locationTyn, next_to=cls.locationTun)
        cls.nextToTunIon = Next_to.objects.create(location=cls.locationTun, next_to=cls.locationIon)
        cls.nextToIonTun = Next_to.objects.create(location=cls.locationIon, next_to=cls.locationTun)
        cls.nextToIonTyn = Next_to.objects.create(location=cls.locationIon, next_to=cls.locationTyn)
        cls.nextToTynIon = Next_to.objects.create(location=cls.locationTyn, next_to=cls.locationIon)
        cls.nextToNapTyn = Next_to.objects.create(location=cls.locationNap, next_to=cls.locationTyn)
        cls.nextToTynNap = Next_to.objects.create(location=cls.locationTyn, next_to=cls.locationNap)
        cls.nextToRomTyn = Next_to.objects.create(location=cls.locationRom, next_to=cls.locationTyn)
        cls.nextToTynRom = Next_to.objects.create(location=cls.locationTyn, next_to=cls.locationRom)
        cls.nextToNapRom = Next_to.objects.create(location=cls.locationNap, next_to=cls.locationRom)
        cls.nextToRomNap = Next_to.objects.create(location=cls.locationRom, next_to=cls.locationNap)
        cls.nextToNapIon = Next_to.objects.create(location=cls.locationNap, next_to=cls.locationIon)
        cls.nextToIonNap = Next_to.objects.create(location=cls.locationIon, next_to=cls.locationNap)
        cls.nextToApuIon = Next_to.objects.create(location=cls.locationApu, next_to=cls.locationIon)
        cls.nextToIonApu = Next_to.objects.create(location=cls.locationIon, next_to=cls.locationApu)
        cls.nextToApuRom = Next_to.objects.create(location=cls.locationApu, next_to=cls.locationRom)
        cls.nextToRomApu = Next_to.objects.create(location=cls.locationRom, next_to=cls.locationApu)
        cls.nextToApuNap = Next_to.objects.create(location=cls.locationApu, next_to=cls.locationNap)
        cls.nextToNapApu = Next_to.objects.create(location=cls.locationNap, next_to=cls.locationApu)

        # Country
        cls.france = Country.objects.create(name="country A", map=cls.map,colour='red')
        cls.italy = Country.objects.create(name="country B", map=cls.map,colour='black')
        cls.germany = Country.objects.create(name="country C", map=cls.map,colour='grey')


    def test_convoy_diagram_30(self):
        # A Tun–Nap - bounce/fail
        # F Tyn C A Tun–Nap - ncvy
        # F Ion–Tyn - maybe
        # F Nap S F Ion–Tyn - maybe 
        unitA = Unit.objects.create(owner=self.france,location=self.locationTun)
        unitB = Unit.objects.create(owner=self.france,location=self.locationTyn,can_float=True)
        unitC = Unit.objects.create(owner=self.italy,location=self.locationIon,can_float=True)
        unitD = Unit.objects.create(owner=self.italy,location=self.locationNap,can_float=True)

        order_1 = Order(instruction=MoveType.MOVE,turn=self.turn,
                                target_unit=unitA,current_location=self.locationTun,
                                target_location=self.locationNap)
        self.assertTrue(order_1.save())
        order_2 = Order(instruction=MoveType.CONVOY,turn=self.turn,
                                target_unit=unitB,current_location=self.locationTyn,
                                reference_unit=unitA,
                                reference_unit_current_location=self.locationTun,
                                reference_unit_new_location=self.locationNap)
        self.assertTrue(order_2.save())

        order_3 = Order(instruction=MoveType.MOVE,turn=self.turn,
                                target_unit=unitC,current_location=self.locationIon,
                                target_location=self.locationTyn)
        self.assertTrue(order_3.save())
        order_4 = Order(instruction=MoveType.SUPPORT,turn=self.turn,
                                target_unit=unitD,current_location=self.locationNap,
                                reference_unit=unitC,
                                reference_unit_current_location=self.locationIon,
                                reference_unit_new_location=self.locationTyn)
        self.assertTrue(order_4.save())
        LegitamiseOrders(self.turn)
        ResolveOrders(self.turn)
        outcome_1 = Outcome.objects.get(order_reference=order_1)
        if type(outcome_1) is Outcome:
            self.assertEqual(outcome_1.validation, OutcomeType.BOUNCE)
        outcome_2 = Outcome.objects.get(order_reference=order_2)
        if type(outcome_2) is Outcome:
            self.assertEqual(outcome_2.validation, OutcomeType.NO_CONVOY)
        outcome_3 = Outcome.objects.get(order_reference=order_3)
        if type(outcome_3) is Outcome:
            self.assertEqual(outcome_3.validation, OutcomeType.MAYBE)
        outcome_4 = Outcome.objects.get(order_reference=order_4)
        if type(outcome_4) is Outcome:
            self.assertEqual(outcome_4.validation, OutcomeType.MAYBE)

    def test_convoy_diagram_31(self):
        # A Tun–Nap - bounce
        # F Tyn C A Tun–Nap - no_cvy 
        # F Ion C A Tun–Nap - maybe 
        # F Rom–Tyn - bounce
        # F Nap S F Rom–Tyn - cut
        unitA = Unit.objects.create(owner=self.france,location=self.locationTun)
        unitB = Unit.objects.create(owner=self.france,location=self.locationTyn,can_float=True)
        unitC = Unit.objects.create(owner=self.france,location=self.locationIon,can_float=True)
        unitD = Unit.objects.create(owner=self.italy,location=self.locationRom,can_float=True)
        unitE = Unit.objects.create(owner=self.italy,location=self.locationNap,can_float=True)

        order_1 = Order(instruction=MoveType.MOVE,turn=self.turn,
                                target_unit=unitA,current_location=self.locationTun,
                                target_location=self.locationNap)
        self.assertTrue(order_1.save())
        order_2 = Order(instruction=MoveType.CONVOY,turn=self.turn,
                                target_unit=unitB,current_location=self.locationTyn,
                                reference_unit=unitA,
                                reference_unit_current_location=self.locationTun,
                                reference_unit_new_location=self.locationNap)
        self.assertTrue(order_2.save())
        order_3 = Order(instruction=MoveType.CONVOY,turn=self.turn,
                                target_unit=unitC,current_location=self.locationIon,
                                reference_unit=unitA,
                                reference_unit_current_location=self.locationTun,
                                reference_unit_new_location=self.locationNap)
        self.assertTrue(order_3.save())

        order_4 = Order(instruction=MoveType.MOVE,turn=self.turn,
                                target_unit=unitD,current_location=self.locationRom,
                                target_location=self.locationTyn)
        self.assertTrue(order_4.save())
        order_5 = Order(instruction=MoveType.SUPPORT,turn=self.turn,
                                target_unit=unitE,current_location=self.locationNap,
                                reference_unit=unitD,
                                reference_unit_current_location=self.locationRom,
                                reference_unit_new_location=self.locationTyn)
        self.assertTrue(order_5.save())
        LegitamiseOrders(self.turn)
        ResolveOrders(self.turn)
        outcome_1 = Outcome.objects.get(order_reference=order_1)
        if type(outcome_1) is Outcome:
            self.assertEqual(outcome_1.validation, OutcomeType.BOUNCE)
        outcome_2 = Outcome.objects.get(order_reference=order_2)
        if type(outcome_2) is Outcome:
            self.assertEqual(outcome_2.validation, OutcomeType.NO_CONVOY)
        outcome_3 = Outcome.objects.get(order_reference=order_3)
        if type(outcome_3) is Outcome:
            self.assertEqual(outcome_3.validation, OutcomeType.MAYBE)
        outcome_4 = Outcome.objects.get(order_reference=order_4)
        if type(outcome_4) is Outcome:
            self.assertEqual(outcome_4.validation, OutcomeType.BOUNCE)
        outcome_5 = Outcome.objects.get(order_reference=order_5)
        if type(outcome_5) is Outcome:
            self.assertEqual(outcome_5.validation, OutcomeType.CUT)
    
    def test_convoy_diagram_32(self):
        # A Tun–Nap - mayb
        # F Tyn C A Tun–Nap - no_cvy? 
        # F Ion C A Tun–Nap - maybe?
        # A Apu S A Tun–Nap - maybe
        # F Rom–Tyn - bounce
        # F Nap S F Rom–Tyn - cut then dislodge
        unitA = Unit.objects.create(owner=self.france,location=self.locationTun)
        unitB = Unit.objects.create(owner=self.france,location=self.locationTyn,can_float=True)
        unitC = Unit.objects.create(owner=self.france,location=self.locationIon,can_float=True)
        unitD = Unit.objects.create(owner=self.france,location=self.locationApu)
        unitE = Unit.objects.create(owner=self.italy,location=self.locationRom,can_float=True)
        unitF = Unit.objects.create(owner=self.italy,location=self.locationNap,can_float=True)

        order_1 = Order(instruction=MoveType.MOVE,turn=self.turn,
                                target_unit=unitA,current_location=self.locationTun,
                                target_location=self.locationNap)
        self.assertTrue(order_1.save())
        order_2 = Order(instruction=MoveType.CONVOY,turn=self.turn,
                                target_unit=unitB,current_location=self.locationTyn,
                                reference_unit=unitA,
                                reference_unit_current_location=self.locationTun,
                                reference_unit_new_location=self.locationNap)
        self.assertTrue(order_2.save())
        order_3 = Order(instruction=MoveType.CONVOY,turn=self.turn,
                                target_unit=unitC,current_location=self.locationIon,
                                reference_unit=unitA,
                                reference_unit_current_location=self.locationTun,
                                reference_unit_new_location=self.locationNap)
        self.assertTrue(order_3.save())
        order_4 = Order(instruction=MoveType.SUPPORT,turn=self.turn,
                                target_unit=unitD,current_location=self.locationApu,
                                reference_unit=unitA,
                                reference_unit_current_location=self.locationTun,
                                reference_unit_new_location=self.locationNap)
        self.assertTrue(order_4.save())
    

        order_5 = Order(instruction=MoveType.MOVE,turn=self.turn,
                                target_unit=unitE,current_location=self.locationRom,
                                target_location=self.locationTyn)
        self.assertTrue(order_5.save())
        order_6 = Order(instruction=MoveType.SUPPORT,turn=self.turn,
                                target_unit=unitF,current_location=self.locationNap,
                                reference_unit=unitE,
                                reference_unit_current_location=self.locationRom,
                                reference_unit_new_location=self.locationTyn)
        self.assertTrue(order_6.save())
        LegitamiseOrders(self.turn)
        ResolveOrders(self.turn)
        outcome_1 = Outcome.objects.get(order_reference=order_1)
        if type(outcome_1) is Outcome:
            self.assertEqual(outcome_1.validation, OutcomeType.MAYBE)
        outcome_2 = Outcome.objects.get(order_reference=order_2)
        if type(outcome_2) is Outcome:
            self.assertEqual(outcome_2.validation, OutcomeType.NO_CONVOY)
        outcome_3 = Outcome.objects.get(order_reference=order_3)
        if type(outcome_3) is Outcome:
            self.assertEqual(outcome_3.validation, OutcomeType.MAYBE)
        outcome_4 = Outcome.objects.get(order_reference=order_4)
        if type(outcome_4) is Outcome:
            self.assertEqual(outcome_4.validation, OutcomeType.MAYBE)
        outcome_5 = Outcome.objects.get(order_reference=order_5)
        if type(outcome_5) is Outcome:
            self.assertEqual(outcome_5.validation, OutcomeType.BOUNCE)
        outcome_6 = Outcome.objects.get(order_reference=order_6)
        if type(outcome_6) is Outcome:
            self.assertEqual(outcome_6.validation, OutcomeType.DISLODGED)