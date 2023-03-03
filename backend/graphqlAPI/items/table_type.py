from graphene_django import DjangoObjectType
from backend.room.models.tables import Location, Order, Unit, Outcome, Turn

# allow access overall parameters
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







