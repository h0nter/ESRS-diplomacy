from django.contrib import admin
# from .models.graph_demo import Category, Book, Grocery
from .models.tables import Unit, Location, Next_to, Map, Country, Order, Outcome, Turn

# Register your models here.
admin.site.register(Country)
admin.site.register(Location)
admin.site.register(Next_to)
admin.site.register(Map)
admin.site.register(Order)
admin.site.register(Outcome)
admin.site.register(Unit)
admin.site.register(Turn)
