from graphene import ObjectType, Union, List
from graphene_django import DjangoObjectType
from room.models.locations import Location, Map, Country, Map_Polygon, Next_to
from room.models.order import Order, Turn, Outcome
from room.game.unitTypes import Army, Fleet

# allow access overall parameters
class LocationType(DjangoObjectType):
    class Meta: 
        model = Location
        fields = "__all__"

class OrderType(DjangoObjectType):
    class Meta: 
        model = Order
        fields = "__all__"

class ArmyType(DjangoObjectType):
    class Meta: 
        model = Army
        fields = "__all__"

class FleetType(DjangoObjectType):
    class Meta: 
        model = Fleet
        fields = "__all__" 

class UnitUnion(Union):
    @classmethod
    def resolve_type(cls, instance, info):
		# This function tells Graphene what Graphene type the instance is
        if isinstance(instance, Army):
            return ArmyType
        if isinstance(instance, Fleet):
            return FleetType
        return UnitUnion.resolve_type(instance, info)

    class Meta: 
        types = (ArmyType, FleetType)

class UnitType(ObjectType):
    all_posts = List(UnitUnion)

    def resolve_all_posts(self, info):
        return list(Army.objects.all()) + list(Fleet.objects.all())

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

