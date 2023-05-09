from django.db import models
from .location import Location
from .country import Country
from .room import Room


class LocationOwner(models.Model):
    room = models.ForeignKey(Room, on_delete=models.DO_NOTHING)
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING, related_name='location_for_player')
    current_owner = models.ForeignKey(Country, blank=True, null=True, on_delete=models.DO_NOTHING)
