# Create your tests here.
from django.test import TestCase
from room.models.unit import Unit
from room.game.legitamiseOrders import LegitamiseOrders
from room.game.resolveOrders import ResolveOrders
from room.models.locations import Country, Map, Location, Next_to
from room.models.order import MoveType, Order
from room.models.outcome import Outcome, OutcomeType
from room.models.turn import Turn
from room.models.room import Room

# https://docs.djangoproject.com/en/4.1/topics/testing/tools/#django.test.TestCase 
class room_app_test_resolve_orders_complex_conflict(TestCase):
    # setup test database to use throughout this class
    @classmethod
    def setUpTestData(cls):
        cls.turn = Turn.objects.create(year=1994)
        cls.map = Map.objects.create(name="A test map", max_countries=7)
        cls.room = Room.objects.create(current_turn=cls.turn,room_name='test Room')

        # Locations
        cls.locationBer = Location.objects.create(name="location Ber",map=cls.map)
        cls.locationPru = Location.objects.create(name="location Pru",map=cls.map)
        cls.locationWar = Location.objects.create(name="location War",map=cls.map)
        cls.locationSil = Location.objects.create(name="location Sil",map=cls.map)
        cls.locationBoh = Location.objects.create(name="location Boh",map=cls.map)
        cls.locationTyr = Location.objects.create(name="location Tyr",map=cls.map)
        cls.locationMun = Location.objects.create(name="location Mun",map=cls.map)

        cls.locationTun = Location.objects.create(name='location Tun',map=cls.map,is_coast=True)
        cls.locationTyn = Location.objects.create(name='location Tyn',map=cls.map,is_sea=True)
        cls.locationRom = Location.objects.create(name='location Rom',map=cls.map,is_coast=True)
        cls.locationNap = Location.objects.create(name='location Nap',map=cls.map,is_coast=True)
        cls.locationIon = Location.objects.create(name='location Ion',map=cls.map,is_sea=True)
        cls.locationApu = Location.objects.create(name='location Ion',map=cls.map,is_coast=True)

        # Next To
        cls.nextToBerPru = Next_to.objects.create(location=cls.locationBer, next_to=cls.locationPru)
        cls.nextToPruBer = Next_to.objects.create(location=cls.locationPru, next_to=cls.locationBer)
        cls.nextToBerSil = Next_to.objects.create(location=cls.locationBer, next_to=cls.locationSil)
        cls.nextToSilBer = Next_to.objects.create(location=cls.locationSil, next_to=cls.locationBer)
        cls.nextToBerMun = Next_to.objects.create(location=cls.locationBer, next_to=cls.locationMun)
        cls.nextToMunBer = Next_to.objects.create(location=cls.locationMun, next_to=cls.locationBer)
        cls.nextToTyrMun = Next_to.objects.create(location=cls.locationTyr, next_to=cls.locationMun)
        cls.nextToMunTyr = Next_to.objects.create(location=cls.locationMun, next_to=cls.locationTyr)
        cls.nextToBohMun = Next_to.objects.create(location=cls.locationBoh, next_to=cls.locationMun)
        cls.nextToMunBoh = Next_to.objects.create(location=cls.locationMun, next_to=cls.locationBoh)
        cls.nextToSilMun = Next_to.objects.create(location=cls.locationSil, next_to=cls.locationMun)
        cls.nextToMunSil = Next_to.objects.create(location=cls.locationMun, next_to=cls.locationSil)
        cls.nextToTyrBoh = Next_to.objects.create(location=cls.locationTyr, next_to=cls.locationBoh)
        cls.nextToBohTyr = Next_to.objects.create(location=cls.locationBoh, next_to=cls.locationTyr)
        cls.nextToBohSil = Next_to.objects.create(location=cls.locationBoh, next_to=cls.locationSil)
        cls.nextToSilBoh = Next_to.objects.create(location=cls.locationSil, next_to=cls.locationBoh)
        cls.nextToWarSil = Next_to.objects.create(location=cls.locationWar, next_to=cls.locationSil)
        cls.nextToSilWar = Next_to.objects.create(location=cls.locationSil, next_to=cls.locationWar)
        cls.nextToWarPru = Next_to.objects.create(location=cls.locationWar, next_to=cls.locationPru)
        cls.nextToPruWar = Next_to.objects.create(location=cls.locationPru, next_to=cls.locationWar)
        cls.nextToSilPru = Next_to.objects.create(location=cls.locationSil, next_to=cls.locationPru)
        cls.nextToPruSil = Next_to.objects.create(location=cls.locationPru, next_to=cls.locationSil)

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
        unitA = Unit.objects.create(owner=self.france,location=self.locationTun,room=self.room)
        unitB = Unit.objects.create(owner=self.france,location=self.locationTyn,can_float=True,room=self.room)
        unitC = Unit.objects.create(owner=self.italy,location=self.locationIon,can_float=True,room=self.room)
        unitD = Unit.objects.create(owner=self.italy,location=self.locationNap,can_float=True,room=self.room)

        order_1 = Order(instruction=MoveType.MOVE,turn=self.turn, room=self.room,
                                unit=unitA,current_location=self.locationTun,
                                target_location=self.locationNap)
        self.assertTrue(order_1.save())
        order_2 = Order(instruction=MoveType.CONVOY,turn=self.turn, room=self.room,
                                unit=unitB,current_location=self.locationTyn,
                                reference_unit=unitA,
                                reference_unit_current_location=self.locationTun,
                                reference_unit_new_location=self.locationNap)
        self.assertTrue(order_2.save())

        order_3 = Order(instruction=MoveType.MOVE,turn=self.turn, room=self.room,
                                unit=unitC,current_location=self.locationIon,
                                target_location=self.locationTyn)
        self.assertTrue(order_3.save())
        order_4 = Order(instruction=MoveType.SUPPORT,turn=self.turn, room=self.room,
                                unit=unitD,current_location=self.locationNap,
                                reference_unit=unitC,
                                reference_unit_current_location=self.locationIon,
                                reference_unit_new_location=self.locationTyn)
        self.assertTrue(order_4.save())
        LegitamiseOrders(self.turn,self.room)
        ResolveOrders(self.turn,self.room)
        outcome_1 = Outcome.objects.get(order_reference=order_1)
        if type(outcome_1) is Outcome:
            self.assertEqual(outcome_1.validation, OutcomeType.BOUNCE)
        outcome_2 = Outcome.objects.get(order_reference=order_2)
        if type(outcome_2) is Outcome:
            self.assertEqual(outcome_2.validation, OutcomeType.DISRUPTED)
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
        unitA = Unit.objects.create(owner=self.france,location=self.locationTun,room=self.room)
        unitB = Unit.objects.create(owner=self.france,location=self.locationTyn,can_float=True,room=self.room)
        unitC = Unit.objects.create(owner=self.france,location=self.locationIon,can_float=True,room=self.room)
        unitD = Unit.objects.create(owner=self.italy,location=self.locationRom,can_float=True,room=self.room)
        unitE = Unit.objects.create(owner=self.italy,location=self.locationNap,can_float=True,room=self.room)

        order_1 = Order(instruction=MoveType.MOVE,turn=self.turn, room=self.room,
                                unit=unitA,current_location=self.locationTun,
                                target_location=self.locationNap)
        self.assertTrue(order_1.save())
        order_2 = Order(instruction=MoveType.CONVOY,turn=self.turn, room=self.room,
                                unit=unitB,current_location=self.locationTyn,
                                reference_unit=unitA,
                                reference_unit_current_location=self.locationTun,
                                reference_unit_new_location=self.locationNap)
        self.assertTrue(order_2.save())
        order_3 = Order(instruction=MoveType.CONVOY,turn=self.turn, room=self.room,
                                unit=unitC,current_location=self.locationIon,
                                reference_unit=unitA,
                                reference_unit_current_location=self.locationTun,
                                reference_unit_new_location=self.locationNap)
        self.assertTrue(order_3.save())

        order_4 = Order(instruction=MoveType.MOVE,turn=self.turn, room=self.room,
                                unit=unitD,current_location=self.locationRom,
                                target_location=self.locationTyn)
        self.assertTrue(order_4.save())
        order_5 = Order(instruction=MoveType.SUPPORT,turn=self.turn, room=self.room,
                                unit=unitE,current_location=self.locationNap,
                                reference_unit=unitD,
                                reference_unit_current_location=self.locationRom,
                                reference_unit_new_location=self.locationTyn)
        self.assertTrue(order_5.save())
        LegitamiseOrders(self.turn,self.room)
        ResolveOrders(self.turn,self.room)
        outcome_1 = Outcome.objects.get(order_reference=order_1)
        if type(outcome_1) is Outcome:
            self.assertEqual(outcome_1.validation, OutcomeType.BOUNCE)
        outcome_2 = Outcome.objects.get(order_reference=order_2)
        if type(outcome_2) is Outcome:
            self.assertEqual(outcome_2.validation, OutcomeType.DISRUPTED)
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
        unitA = Unit.objects.create(owner=self.france,location=self.locationTun,room=self.room)
        unitB = Unit.objects.create(owner=self.france,location=self.locationTyn,can_float=True,room=self.room)
        unitC = Unit.objects.create(owner=self.france,location=self.locationIon,can_float=True,room=self.room)
        unitD = Unit.objects.create(owner=self.france,location=self.locationApu,room=self.room)
        unitE = Unit.objects.create(owner=self.italy,location=self.locationRom,can_float=True,room=self.room)
        unitF = Unit.objects.create(owner=self.italy,location=self.locationNap,can_float=True,room=self.room)

        order_1 = Order(instruction=MoveType.MOVE,turn=self.turn, room=self.room,
                                unit=unitA,current_location=self.locationTun,
                                target_location=self.locationNap)
        self.assertTrue(order_1.save())
        order_2 = Order(instruction=MoveType.CONVOY,turn=self.turn, room=self.room,
                                unit=unitB,current_location=self.locationTyn,
                                reference_unit=unitA,
                                reference_unit_current_location=self.locationTun,
                                reference_unit_new_location=self.locationNap)
        self.assertTrue(order_2.save())
        order_3 = Order(instruction=MoveType.CONVOY,turn=self.turn, room=self.room,
                                unit=unitC,current_location=self.locationIon,
                                reference_unit=unitA,
                                reference_unit_current_location=self.locationTun,
                                reference_unit_new_location=self.locationNap)
        self.assertTrue(order_3.save())
        order_4 = Order(instruction=MoveType.SUPPORT,turn=self.turn, room=self.room,
                                unit=unitD,current_location=self.locationApu,
                                reference_unit=unitA,
                                reference_unit_current_location=self.locationTun,
                                reference_unit_new_location=self.locationNap)
        self.assertTrue(order_4.save())
    

        order_5 = Order(instruction=MoveType.MOVE,turn=self.turn, room=self.room,
                                unit=unitE,current_location=self.locationRom,
                                target_location=self.locationTyn)
        self.assertTrue(order_5.save())
        order_6 = Order(instruction=MoveType.SUPPORT,turn=self.turn, room=self.room,
                                unit=unitF,current_location=self.locationNap,
                                reference_unit=unitE,
                                reference_unit_current_location=self.locationRom,
                                reference_unit_new_location=self.locationTyn)
        self.assertTrue(order_6.save())
        LegitamiseOrders(self.turn,self.room)
        ResolveOrders(self.turn,self.room)
        outcome_1 = Outcome.objects.get(order_reference=order_1)
        if type(outcome_1) is Outcome:
            self.assertEqual(outcome_1.validation, OutcomeType.MAYBE)
        outcome_2 = Outcome.objects.get(order_reference=order_2)
        if type(outcome_2) is Outcome:
            self.assertEqual(outcome_2.validation, OutcomeType.DISRUPTED)
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

    def test_diagram_12(self):
        # A Boh–Mun; - maybe
        # A Tyr S A Boh–Mun - maybe
        # A Mun–Sil; - bounce then dislodge
        # A Ber S A Mun–Si - maybe
        # A War–Sil; - bounce
        # A Pru S A War–Sil - maybe
        unitA = Unit.objects.create(owner=self.france,location=self.locationBoh,room=self.room)
        unitB = Unit.objects.create(owner=self.france,location=self.locationTyr,room=self.room)
        unitC = Unit.objects.create(owner=self.germany,location=self.locationMun,room=self.room)
        unitD = Unit.objects.create(owner=self.germany,location=self.locationBer,room=self.room)
        unitE = Unit.objects.create(owner=self.italy,location=self.locationWar,room=self.room)
        unitF = Unit.objects.create(owner=self.italy,location=self.locationPru,room=self.room)

        order_1 = Order(instruction=MoveType.MOVE,turn=self.turn, room=self.room,
                                unit=unitA,current_location=self.locationBoh,
                                target_location=self.locationMun)
        self.assertTrue(order_1.save())
        order_2 = Order(instruction=MoveType.SUPPORT,turn=self.turn, room=self.room,
                                unit=unitB,current_location=self.locationTyr,
                                reference_unit=unitA,
                                reference_unit_current_location=self.locationBoh,
                                reference_unit_new_location=self.locationMun)
        self.assertTrue(order_2.save())

        order_3 = Order(instruction=MoveType.MOVE,turn=self.turn, room=self.room,
                                unit=unitC,current_location=self.locationMun,
                                target_location=self.locationSil)
        self.assertTrue(order_3.save())
        order_4 = Order(instruction=MoveType.SUPPORT,turn=self.turn, room=self.room,
                                unit=unitD,current_location=self.locationBer,
                                reference_unit=unitC,
                                reference_unit_current_location=self.locationMun,
                                reference_unit_new_location=self.locationSil)
        self.assertTrue(order_4.save())

        order_5 = Order(instruction=MoveType.MOVE,turn=self.turn, room=self.room,
                                unit=unitE,current_location=self.locationWar,
                                target_location=self.locationSil)
        self.assertTrue(order_5.save())
        order_6 = Order(instruction=MoveType.SUPPORT,turn=self.turn, room=self.room,
                                unit=unitF,current_location=self.locationPru,
                                reference_unit=unitE,
                                reference_unit_current_location=self.locationWar,
                                reference_unit_new_location=self.locationSil)
        self.assertTrue(order_6.save())
        LegitamiseOrders(self.turn,self.room)
        ResolveOrders(self.turn,self.room)
        outcome_1 = Outcome.objects.get(order_reference=order_1)
        if type(outcome_1) is Outcome:
            self.assertEqual(outcome_1.validation, OutcomeType.MAYBE)
        outcome_2 = Outcome.objects.get(order_reference=order_2)
        if type(outcome_2) is Outcome:
            self.assertEqual(outcome_2.validation, OutcomeType.MAYBE)
        outcome_3 = Outcome.objects.get(order_reference=order_3)
        if type(outcome_3) is Outcome:
            self.assertEqual(outcome_3.validation, OutcomeType.DISLODGED)
        outcome_4 = Outcome.objects.get(order_reference=order_4)
        if type(outcome_4) is Outcome:
            self.assertEqual(outcome_4.validation, OutcomeType.MAYBE)
        outcome_5 = Outcome.objects.get(order_reference=order_5)
        if type(outcome_5) is Outcome:
            self.assertEqual(outcome_5.validation, OutcomeType.BOUNCE)
        outcome_6 = Outcome.objects.get(order_reference=order_6)
        if type(outcome_6) is Outcome:
            self.assertEqual(outcome_6.validation, OutcomeType.MAYBE)

    def test_diagram_13(self):
        # A Bul–Rum ->         A Mun-Sil
        # A Rum–Bul ->         A Sil-Mun
        # A Ser S A Rum–Bul -> A Boh S A Sil-Mun
        # A Sev–Rum ->         A War-Sil
        unitA = Unit.objects.create(owner=self.france,location=self.locationMun,room=self.room)
        unitB = Unit.objects.create(owner=self.germany,location=self.locationSil,room=self.room)
        unitC = Unit.objects.create(owner=self.germany,location=self.locationBoh,room=self.room)
        unitD = Unit.objects.create(owner=self.germany,location=self.locationWar,room=self.room)

        order_1 = Order(instruction=MoveType.MOVE,turn=self.turn, room=self.room,
                                unit=unitA,current_location=self.locationMun,
                                target_location=self.locationSil)
        self.assertTrue(order_1.save())

        order_2 = Order(instruction=MoveType.MOVE,turn=self.turn, room=self.room,
                                unit=unitB,current_location=self.locationSil,
                                target_location=self.locationMun)
        self.assertTrue(order_2.save())
        order_3 = Order(instruction=MoveType.SUPPORT,turn=self.turn, room=self.room,
                                unit=unitC,current_location=self.locationBoh,
                                reference_unit=unitB,
                                reference_unit_current_location=self.locationSil,
                                reference_unit_new_location=self.locationMun)
        self.assertTrue(order_3.save())
        order_4 = Order(instruction=MoveType.MOVE,turn=self.turn, room=self.room,
                                unit=unitD,current_location=self.locationWar,
                                target_location=self.locationSil)
        self.assertTrue(order_4.save())

        LegitamiseOrders(self.turn,self.room)
        ResolveOrders(self.turn,self.room)
        outcome_1 = Outcome.objects.get(order_reference=order_1)
        if type(outcome_1) is Outcome:
            self.assertEqual(outcome_1.validation, OutcomeType.DISLODGED)
        outcome_2 = Outcome.objects.get(order_reference=order_2)
        if type(outcome_2) is Outcome:
            self.assertEqual(outcome_2.validation, OutcomeType.MAYBE)
        outcome_3 = Outcome.objects.get(order_reference=order_3)
        if type(outcome_3) is Outcome:
            self.assertEqual(outcome_3.validation, OutcomeType.MAYBE)
        outcome_4 = Outcome.objects.get(order_reference=order_4)
        if type(outcome_4) is Outcome:
            self.assertEqual(outcome_4.validation, OutcomeType.MAYBE)

    def test_diagram_14(self):
        # A Bul–Rum             -> A Boh-Sil - Dislodged
        # F Bla S A Bul–Rum     -> A War S A Boh-Sil - maybe/void?
        # A Rum–Bul;            -> A Sil-Boh - maybe
        # A Gre S A Rum–Bul;    -> A Tyr S A Sil-Boh - maybe
        # A Ser S A Rum–Bul;    -> A Mun S A Sil-Boh - maybe
        # A Sev–Rum             -> A Pru-Sil - maybe

        unitA = Unit.objects.create(owner=self.france,location=self.locationBoh,room=self.room)
        unitB = Unit.objects.create(owner=self.france,location=self.locationWar,room=self.room)
        unitC = Unit.objects.create(owner=self.germany,location=self.locationSil,room=self.room)
        unitD = Unit.objects.create(owner=self.germany,location=self.locationTyr,room=self.room)
        unitE = Unit.objects.create(owner=self.germany,location=self.locationMun,room=self.room)
        unitF = Unit.objects.create(owner=self.germany,location=self.locationPru,room=self.room)

        order_1 = Order(instruction=MoveType.MOVE,turn=self.turn, room=self.room,
                                unit=unitA,current_location=self.locationBoh,
                                target_location=self.locationSil)
        self.assertTrue(order_1.save())
        order_2 = Order(instruction=MoveType.SUPPORT,turn=self.turn, room=self.room,
                                unit=unitB,current_location=self.locationWar,
                                reference_unit=unitA,
                                reference_unit_current_location=self.locationBoh,
                                reference_unit_new_location=self.locationSil)
        self.assertTrue(order_2.save())

        order_3 = Order(instruction=MoveType.MOVE,turn=self.turn, room=self.room,
                                unit=unitC,current_location=self.locationSil,
                                target_location=self.locationBoh)
        self.assertTrue(order_3.save())
        order_4 = Order(instruction=MoveType.SUPPORT,turn=self.turn, room=self.room,
                                unit=unitD,current_location=self.locationTyr,
                                reference_unit=unitC,
                                reference_unit_current_location=self.locationSil,
                                reference_unit_new_location=self.locationBoh)
        self.assertTrue(order_4.save())
        order_5 = Order(instruction=MoveType.SUPPORT,turn=self.turn, room=self.room,
                                unit=unitE,current_location=self.locationMun,
                                reference_unit=unitC,
                                reference_unit_current_location=self.locationSil,
                                reference_unit_new_location=self.locationBoh)
        self.assertTrue(order_5.save())
        order_6 = Order(instruction=MoveType.MOVE,turn=self.turn, room=self.room,
                                unit=unitF,current_location=self.locationPru,
                                target_location=self.locationSil)
        self.assertTrue(order_6.save())
        LegitamiseOrders(self.turn,self.room)
        ResolveOrders(self.turn,self.room)
        outcome_1 = Outcome.objects.get(order_reference=order_1)
        if type(outcome_1) is Outcome:
            self.assertEqual(outcome_1.validation, OutcomeType.DISLODGED)
        outcome_2 = Outcome.objects.get(order_reference=order_2)
        if type(outcome_2) is Outcome:
            self.assertEqual(outcome_2.validation, OutcomeType.MAYBE) #void?
        outcome_3 = Outcome.objects.get(order_reference=order_3)
        if type(outcome_3) is Outcome:
            self.assertEqual(outcome_3.validation, OutcomeType.MAYBE)
        outcome_4 = Outcome.objects.get(order_reference=order_4)
        if type(outcome_4) is Outcome:
            self.assertEqual(outcome_4.validation, OutcomeType.MAYBE)
        outcome_5 = Outcome.objects.get(order_reference=order_5)
        if type(outcome_5) is Outcome:
            self.assertEqual(outcome_5.validation, OutcomeType.MAYBE)
        outcome_6 = Outcome.objects.get(order_reference=order_6)
        if type(outcome_6) is Outcome:
            self.assertEqual(outcome_6.validation, OutcomeType.MAYBE)