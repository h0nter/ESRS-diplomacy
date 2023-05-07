from django.contrib import admin
from room.models.location import Location, Next_to, Map_Polygon
from room.models.map import Map
from room.models.country import Country
from room.models.order import Order
from room.models.turn import Turn
from room.models.outcome import Outcome
from room.models.player import Player
from room.models.unit import Unit


# Register your models here.
admin.site.register(Country)
admin.site.register(Location)
admin.site.register(Next_to)
admin.site.register(Map_Polygon)
admin.site.register(Map)
admin.site.register(Order)
admin.site.register(Outcome)
admin.site.register(Unit)
admin.site.register(Turn)
admin.site.register(Player)