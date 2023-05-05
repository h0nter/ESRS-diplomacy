from django.contrib.auth.models import User
from graphene_django import DjangoObjectType
from room.models.locations import Location, Map, Country, Map_Polygon, Next_to
from room.models.order import Order, Turn, Outcome
from room.game.unitTypes import Unit
from room.models.player import Player
from room.models.room import Room


# set access fields, in different models
class LocationType(DjangoObjectType):
    class Meta: 
        model = Location
        fields = "__all__"

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


class Map_PolygonType(DjangoObjectType):
    class Meta: 
        model = Map_Polygon
        fields = "__all__"

class Next_toType(DjangoObjectType):
    class Meta: 
        model = Next_to
        fields = "__all__"

class UserType(DjangoObjectType):
    class Meta: 
        model = User
        fields = ["username", "id", "is_staff"]

class PlayerType(DjangoObjectType):
    class Meta: 
        model = Player
        fields = "__all__"

class RoomType(DjangoObjectType):
    class Meta: 
        model = Room
        fields = "__all__"