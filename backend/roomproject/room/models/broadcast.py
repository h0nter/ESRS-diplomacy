from django.db import models
from .room import Room
from .order import Turn
from .order import Order
from .order import Outcome


class OrderBroadcast(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="OrderBroadcast_room")
    turn = models.ForeignKey(Turn, on_delete=models.CASCADE, related_name="OrderBroadcast_turn")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="OrderBroadcast_order")


class OutcomeBroadcast(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="OutcomeBroadcast_room")
    turn = models.ForeignKey(Turn, on_delete=models.CASCADE, related_name="OutcomeBroadcast_turn")
    outcome = models.ForeignKey(Outcome, on_delete=models.CASCADE, related_name="OutcomeBroadcast_outcome")
