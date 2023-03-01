import graphene
from graphene_django import DjangoObjectType
from ...room.models.tables import Location
from table_type import LocationType

class UpdateLocation(graphene.Mutation):
    class Arguments:
        # Mutation to update a locaiotn
        id = graphene.ID()
        name = graphene.String(required=True)
        is_sea = graphene.Boolean()

    locaiotn = graphene.Field(LocationType)

    @classmethod
    def mutate(cls, root, info, name, id):
        locaiotn = Location.objects.get(pk=id)
        locaiotn.name = name
        locaiotn.save()
        
        return UpdateLocation(locaiotn=locaiotn)

class CreateLocation(graphene.Mutation):
    class Arguments:
        # Mutation to create a location
        name = graphene.String(required=True)

    # Class attributes define the response of the mutation
    location = graphene.Field(LocationType)

    @classmethod
    def mutate(cls, root, info, name, is_sea):
        location = Location()
        location.name = name
        location.is_sea = is_sea
        location.save()
        
        return CreateLocation(location = location)