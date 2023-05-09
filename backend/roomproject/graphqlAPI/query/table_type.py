from graphene_django import DjangoObjectType
from room.models.location import Location, Map_Polygon, Next_to
from room.models.country import Country
from room.models.map import Map
from room.models.order import Order
from room.models.turn import Turn
from room.models.outcome import Outcome 
from room.models.unit import Unit
from room.models.player import Player
from room.models.room import Room, RoomStatus
import graphene


# class RoomStatusChoices(graphene.Enum):
#     @classmethod
#     def from_enum(cls, enum):
#         return cls(*[(choice.value, choice.name) for choice in enum])
    
#     REGISTERED = RoomStatus.REGISTERED
#     INITIALIZE =  RoomStatus.INITIALIZE
#     WAITING =RoomStatus.WAITING
#     RESOLVE = RoomStatus.RESOLVE
#     RETREAT =RoomStatus.RETREAT
#     UPDATE = RoomStatus.UPDATE
#     RESUPPLY = RoomStatus.RESUPPLY
#     CHECKING = RoomStatus.CHECKING
#     CLOSED = RoomStatus.CLOSED


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


class PlayerType(DjangoObjectType):
    class Meta: 
        model = Player
        fields = "__all__"


class RoomType(DjangoObjectType):
    class Meta: 
        model = Room
        # status = graphene.Field(RoomStatusChoices)
        fields = "__all__"
    
    