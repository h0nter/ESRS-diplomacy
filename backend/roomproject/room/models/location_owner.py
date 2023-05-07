from django.db import models
from .locations import Location, Country
from .room import Room


class LocationOwner():
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING, related_name='location_for_player')
    current_owner = models.ForeignKey(Country, blank=True, null=True, on_delete=models.DO_NOTHING)
    room = models.ForeignKey(Room, on_delete=models.DO_NOTHING)