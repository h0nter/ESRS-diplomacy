from django.contrib import admin
from .models.graph_demo import Category, Book, Grocery

# Register your models here.

admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Grocery)