from django.contrib import admin
from .tables import Unit, Country, Location, Order, Turn, Map, Next_to

# Register your models here.
admin.site.register(Country)
admin.site.register(Location)
admin.site.register(Unit)
admin.site.register(Order)
admin.site.register(Turn)
admin.site.register(Map)
admin.site.register(Next_to)