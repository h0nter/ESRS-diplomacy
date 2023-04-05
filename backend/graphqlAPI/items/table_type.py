from graphene_django import DjangoObjectType, DjangoListField
from room.models.tables import *

# allow access overall parameters
class Map_PolygonType(DjangoObjectType):
    class Meta:
        model = Map_Polygon
        fields = "__all__"

class LocationType(DjangoObjectType):
    polygons = DjangoListField(Map_PolygonType)
    class Meta: 
        model = Location
        fields = ('name', 'unit_spawn', 'is_sea', 'is_coast', 'map', 'text_pos_x', 'text_pos_y', 'current_owner', 'polygons')

class OrderType(DjangoObjectType):
    class Meta: 
        model = Order
        fields = "__all__"

class UnitType(DjangoObjectType):
    class Meta: 
        model = Unit
        fields = "__all__"

class TurnType(DjangoObjectType):
    class Meta: 
        model = Turn
        fields = "__all__"

class OutcomeType(DjangoObjectType):
    class Meta: 
        model = Outcome
        fields = "__all__"

class MapType(DjangoObjectType):
    class Meta: 
        model = Map
        fields = "__all__"

class CountryType(DjangoObjectType):
    class Meta: 
        model = Country
        fields = "__all__"

class Next_toType(DjangoObjectType):
    class Meta: 
        model = Next_to
        fields = "__all__"

