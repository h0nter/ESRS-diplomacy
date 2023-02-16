from django.contrib import admin
from .models.graph_demo import Category, Book, Grocery
from .models.tables import Units, Location

# Register your models here.

admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Grocery)
admin.site.register(Location)
admin.site.register(Units)