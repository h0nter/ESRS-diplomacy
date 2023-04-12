from django.contrib import admin
from room.models.locations import Location, Next_to, Map_Polygon, Map, Country
from room.models.order import Order, Outcome, Turn
from room.game.unitTypes import Unit


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
