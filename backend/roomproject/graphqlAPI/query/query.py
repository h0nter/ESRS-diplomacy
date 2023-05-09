import graphene
from .table_type import *
from room.models.location import Location
from room.models.map import Map
from room.models.country import Country
from room.models.outcome import Outcome
from room.models.unit import Unit
from .broadcast import Broadcast
from room.models.location_owner import LocationOwner


class Query(Broadcast, graphene.ObjectType):

    unit = graphene.List(UnitType, room_id=graphene.ID())
    outcome = graphene.List(OutcomeType)
    location = graphene.List(LocationType, room_id=graphene.ID())
    location_owner = graphene.List(LocationOwnerType, room_id=graphene.ID())
    map = graphene.List(MapType, map_id=graphene.ID())
    country = graphene.List(CountryType)
    map_polygon = graphene.List(Map_PolygonType)
    next_to = graphene.List(Next_toType)

    """
    A Resolver is a method that helps us answer Queries by fetching data for a Field in our Schema.
    Resolvers are lazily executed, so if a field is not included in a query, its resolver will not be executed.
    Each field on an ObjectType in Graphene should have a corresponding resolver method to fetch data.
    """
    
    def resolve_unit(root, info, **kwargs):
        room_id = kwargs.get('room_id')
        if room_id is not None:
            return Unit.objects.filter(room_id=room_id)

        return Unit.objects.all()

    def resolve_outcome(root, info, **kwargs):
        return Outcome.objects.all()
    
    def resolve_location(root, info, **kwargs):
        room_id = kwargs.get('room_id')
        if room_id is not None:
            return Location.objects.filter(room_id=room_id)
        return Location.objects.all()

    def resolve_location_owner(root, info, **kwargs):
        room_id = kwargs.get('room_id')
        if room_id is not None:
            return LocationOwner.objects.filter(room_id=room_id)

        return LocationOwner.objects.all()

    def resolve_map(root, info, **kwargs):
        map_id = kwargs.get('map_id')
        if map_id is not None:
            return Map.objects.filter(pk=map_id)

        return Map.objects.all()

    def resolve_map_polygon(root, info, **kwargs):
        return Map_Polygon.objects.all()

    def resolve_next_to(root, info, **kwargs):
        return Next_to.objects.all()

    def resolve_country(root, info, **kwargs):
        return Country.objects.all()