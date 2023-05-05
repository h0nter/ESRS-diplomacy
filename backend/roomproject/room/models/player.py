from django.db import models
from .room import Room
from .locations import Country


class Player(models.Model):
    user_id = models.PositiveIntegerField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='playr_joined_room')
    country = models.ForeignKey(Country,on_delete=models.DO_NOTHING,null=True, related_name='player_country')
    # conditions for identify is player over the game.
    is_alive = models.BooleanField(default=True)
    # condition for identify is player completed their turn.
    is_finished = models.BooleanField(default=True)