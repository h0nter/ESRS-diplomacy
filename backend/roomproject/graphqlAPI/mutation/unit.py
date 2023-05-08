import graphene
from graphene import Mutation, Boolean, ID
from graphqlAPI.query.table_type import UnitType
from room.models.unit import Unit

class CreateUnit(Mutation):
    class Arguments:
        owner = ID()
        room = ID()
        location = ID()
        can_float =Boolean
    
    unit = graphene.Field(UnitType)

    @staticmethod
    def mutate( root, info, owner, room,location,can_float=False):
        unit = Unit.objects.create(owner=owner, room=room, location=location, can_float=can_float)

        return CreateUnit(unit=unit)
