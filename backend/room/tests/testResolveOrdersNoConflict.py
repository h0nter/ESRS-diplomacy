# Create your tests here.
from django.test import TestCase
from room.game.unitTypes import Unit
from room.game.legitamiseOrders import LegitamiseOrders
from room.game.resolveOrders import ResolveOrders
from room.models.locations import Country, Map, Location, Next_to
from room.models.order import MoveType, Order, Outcome, OutcomeType, Turn

# https://docs.djangoproject.com/en/4.1/topics/testing/tools/#django.test.TestCase 
class room_app_test_resolve_orders_no_conflict(TestCase):
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

        cls.nextToGH = Next_to.objects.create(location=cls.locationG, next_to=cls.locationH)
        cls.nextToHG = Next_to.objects.create(location=cls.locationH, next_to=cls.locationG)
        cls.nextToHJ = Next_to.objects.create(location=cls.locationH, next_to=cls.locationJ)
        cls.nextToJH = Next_to.objects.create(location=cls.locationJ, next_to=cls.locationH)

        # Country
        cls.countryA = Country.objects.create(name="country A", map=cls.map,colour='red')

        # Unit
        cls.unitA = Unit.objects.create(owner=cls.countryA,location=cls.locationA)

        cls.unitB = Unit.objects.create(owner=cls.countryA,location=cls.locationB)

        cls.unitC = Unit.objects.create(owner=cls.countryA,location=cls.locationD)
        cls.unitD = Unit.objects.create(owner=cls.countryA,location=cls.locationF)

        cls.unitE = Unit.objects.create(owner=cls.countryA,location=cls.locationG)
        cls.unitF = Unit.objects.create(owner=cls.countryA,location=cls.locationH,can_float=True)

        # Orders
        # Hold - no outside forces
        cls.Order_1 = Order(instruction=MoveType.HOLD,turn=cls.turn,
                                    target_unit=cls.unitA,current_location=cls.locationA)
        cls.Order_1.save()
        # Move - no outside forces
        cls.Order_2 = Order(instruction=MoveType.MOVE,turn=cls.turn,
                                    target_unit=cls.unitB,current_location=cls.locationB,
                                    target_location=cls.locationC)
        cls.Order_2.save()
        # Support - no outside forces
        cls.Order_3 = Order(instruction=MoveType.MOVE,turn=cls.turn,
                                    target_unit=cls.unitC,current_location=cls.locationD,
                                    target_location=cls.locationE)
        cls.Order_3.save()
        cls.Order_4 = Order(instruction=MoveType.SUPPORT,turn=cls.turn,
                                    target_unit=cls.unitD,current_location=cls.locationF,
                                    reference_unit=cls.unitC,
                                    reference_unit_current_location=cls.locationD,
                                    reference_unit_new_location=cls.locationE)
        cls.Order_4.save()
        # Convoy - no outside forces
        cls.Order_5 = Order(instruction=MoveType.MOVE,turn=cls.turn,
                                    target_unit=cls.unitE,current_location=cls.locationG,
                                    target_location=cls.locationJ)
        cls.Order_5.save()
        cls.Order_6 = Order(instruction=MoveType.CONVOY,turn=cls.turn,
                                    target_unit=cls.unitF,current_location=cls.locationH,
                                    reference_unit=cls.unitE,
                                    reference_unit_current_location=cls.locationG,
                                    reference_unit_new_location=cls.locationJ)
        cls.Order_6.save()
        

    
    def test_check_orders_legit(self):
        self.assertTrue(self.Order_5.save())
        LegitamiseOrders(self.turn)
        for outcome in Outcome.objects.filter(order_reference__turn=self.turn):
            if type(outcome) is Outcome:
                #print('{0} {1}'.format(outcome.order_reference.target_unit.location,outcome.validation))
                self.assertEqual(outcome.validation,OutcomeType.MAYBE) 

    def test_resolve(self):
        LegitamiseOrders(self.turn)
        ResolveOrders(self.turn)
        for outcome in Outcome.objects.filter(order_reference__turn=self.turn):
            if type(outcome) is Outcome:
                print('{0} {1}'.format(outcome.order_reference.target_unit.location,outcome.validation))
                self.assertEqual(outcome.validation,OutcomeType.MAYBE) 