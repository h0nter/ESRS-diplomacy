from django.db import models
from .locations import Location
from .player import Player


class LocationOwner():
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING, related_name='location_for_player')
    current_owner = models.ForeignKey(Player, blank=True, null=True, on_delete=models.DO_NOTHING)