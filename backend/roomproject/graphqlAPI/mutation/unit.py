import graphene
from graphene import Mutation, Int, Boolean
from graphqlAPI.query.table_type import UnitType
from room.models.unit import Unit

class CreateUnit(Mutation):
    class Arguments:
        year = Int(required=True)
        is_autumn = Boolean()
    
    turn = graphene.Field(UnitType)

    @staticmethod
    def mutate( root, info, year, is_autumn=False):
        turn = Unit.objects.create(year=year, is_autumn=is_autumn)

        return CreateUnit(turn=turn)
