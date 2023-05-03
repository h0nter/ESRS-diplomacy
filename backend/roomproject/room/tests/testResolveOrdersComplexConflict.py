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
        cls.countryA = Country.objects.create(name="country A", map=cls.map,colour='red')
        cls.countryB = Country.objects.create(name="country B", map=cls.map,colour='blue')
        cls.countryC = Country.objects.create(name="country C", map=cls.map,colour='green')
