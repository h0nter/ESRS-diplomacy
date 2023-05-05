import graphene
from graphene import Mutation, ID
from graphqlAPI.query.table_type import PlayerType
from room.models.player import Player

class CreatePlayer(Mutation):
    class Arguments:
        user_id = ID(required=True)
        room_id = ID(required=True)
    
    player = graphene.Field(PlayerType)

    @staticmethod
    def mutate(root, info, user_id, room_id):
        player = Player.objects.create(user_id=user_id, room_id=room_id)
        
        return CreatePlayer(player=player)
