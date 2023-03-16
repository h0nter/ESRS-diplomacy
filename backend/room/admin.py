from django.contrib import admin
from .models.tables import *


# Register your models here.
admin.site.register(Country)
admin.site.register(Location)
admin.site.register(Next_to)
admin.site.register(Map)
admin.site.register(Order)
admin.site.register(Outcome)
admin.site.register(Unit)
admin.site.register(Turn)
admin.site.register(Map_Polygon)

