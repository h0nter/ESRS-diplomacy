import graphene
from .table_type import *
from room.models.locations import Map, Country, Location
from room.models.order import Outcome
from room.game.unitTypes import Unit
from .broadcast import GameAPI


class Query(GameAPI):

    unit = graphene.List(UnitType)
    outcome = graphene.List(OutcomeType)
    location = graphene.List(LocationType)
    maps = graphene.List(MapType)
    country = graphene.List(CountryType)
    map_polygon = graphene.List(Map_PolygonType)
    next_to = graphene.List(Next_toType)

    """
    A Resolver is a method that helps us answer Queries by fetching data for a Field in our Schema.
    Resolvers are lazily executed, so if a field is not included in a query, its resolver will not be executed.
    Each field on an ObjectType in Graphene should have a corresponding resolver method to fetch data.
    """
    
    def resolve_units(root, info, **kwargs):
        return Unit.objects.all()

    def resolve_outcomes(root, info, **kwargs):
        return Outcome.objects.all()
    
    def resolve_locations(root, info, **kwargs):
        return Location.objects.all()

    def resolve_maps(root, info, **kwargs):
        return Map.objects.all()

    def resolve_map_polygon(root, info, **kwargs):
        return Map_Polygon.objects.all()

    def resolve_next_to(root, info, **kwargs):
        return Next_to.objects.all()

    def resolve_country(root, info, **kwargs):
        return Country.objects.all()