from django.contrib import admin
from .models.tables import Unit, Location, Next_to, Map, Country, Order, Outcome

# Register your models here.
admin.site.register(Country)
admin.site.register(Location)
admin.site.register(Next_to)
admin.site.register(Map)
admin.site.register(Order)
admin.site.register(Outcome)
admin.site.register(Unit)


