import graphene
from ..room.models.tables import Units, Location
from items.location import LocationType, CreateLocation, UpdateLocation
from items.units import UnitsType, CreateUnits, UpdateUnits


class Query(graphene.ObjectType):
    locations = graphene.List(LocationType)
    units = graphene.List(UnitsType)

    def resolve_locations(root, info, **kwargs):
            # Querying a list
            return Location.objects.all()

    def resolve_units(root, info, **kwargs):
            # Querying a list
            return Units.objects.all()


class Mutation(graphene.ObjectType):
    
    update_location = UpdateLocation.Field()
    create_location = CreateLocation.Field()
    update_units = UpdateUnits.Field()
    create_units = CreateUnits.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)