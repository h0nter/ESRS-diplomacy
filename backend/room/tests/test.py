# Create your tests here.
from django.test import TestCase

class room_app_unitTest1(TestCase):
    def test_insert(self):
        from .initial_insert import InitialInsert as II
        II.all_insert()

    def test_move(self):
        from room.models.tables import Order
        from room.game.unit_factory import UnitFactory
        order = Order.objects.first()
        print(order)
        # army = UnitFactory.build_unit(order)
        # army.move()
        # self.assertEqual(army.location, order.target_location)