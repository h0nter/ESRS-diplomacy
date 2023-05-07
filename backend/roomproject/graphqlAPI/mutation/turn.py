import graphene
from graphene import Mutation, Int, Boolean
from graphqlAPI.query.table_type import TurnType
from room.models.order import Turn

class CreateTurn(Mutation):
    class Arguments:
        year = Int(required=True)
        is_autumn = Boolean()
    
    turn = graphene.Field(TurnType)

    @staticmethod
    def mutate( root, info, year, is_autumn=False):
        turn = Turn.objects.create(year=year, is_autumn=is_autumn)

        return CreateTurn(turn=turn)
