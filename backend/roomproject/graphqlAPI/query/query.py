import graphene
from .table_type import *
from room.models.location import Location
from room.models.map import Map
from room.models.country import Country
from room.models.outcome import Outcome
from room.models.unit import Unit
from .broadcast import Broadcast


class Query(Broadcast, graphene.ObjectType):

    unit = graphene.List(UnitType)
    outcome = graphene.List(OutcomeType)
    location = graphene.List(LocationType)
    map = graphene.List(MapType)
    country = graphene.List(CountryType)
    map_polygon = graphene.List(Map_PolygonType)
    next_to = graphene.List(Next_toType)

    """
    A Resolver is a method that helps us answer Queries by fetching data for a Field in our Schema.
    Resolvers are lazily executed, so if a field is not included in a query, its resolver will not be executed.
    Each field on an ObjectType in Graphene should have a corresponding resolver method to fetch data.
    """
    
    def resolve_unit(root, info, **kwargs):
        return Unit.objects.all()

    def resolve_outcome(root, info, **kwargs):
        return Outcome.objects.all()
    
    def resolve_location(root, info, **kwargs):
        return Location.objects.all()

    def resolve_map(root, info, **kwargs):
        return Map.objects.all()

    def resolve_map_polygon(root, info, **kwargs):
        return Map_Polygon.objects.all()

    def resolve_next_to(root, info, **kwargs):
        return Next_to.objects.all()

    def resolve_country(root, info, **kwargs):
        return Country.objects.all()