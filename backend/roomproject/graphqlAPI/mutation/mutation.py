import graphene
from .player import CreatePlayer
from .room import CreateRoom
from .order import UpdateOrder
from .turn import CreateTurn


class Mutation(graphene.ObjectType):

    update_order = UpdateOrder.Field()
    create_player = CreatePlayer.Field()
    create_room = CreateRoom.Field()
    create_trun = CreateTurn.Field()

