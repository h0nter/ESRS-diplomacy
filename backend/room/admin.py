from django.contrib import admin
from .models.graph_demo import Category, Book, Grocery
from .models.tables import Unit, Country, Location, Order, Turn, Map, Next_to

# Register your models here.
admin.site.register(Country)
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Grocery)
admin.site.register(Location)
admin.site.register(Unit)
admin.site.register(Order)
admin.site.register(Turn)
admin.site.register(Map)
admin.site.register(Next_to)