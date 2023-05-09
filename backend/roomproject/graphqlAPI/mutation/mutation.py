import graphene
from .player import CreatePlayer
from .room import CreateRoom, InitialRoom
from .order import UpdateOrder, CreateOrder
from .turn import CreateTurn
from .unit import CreateUnit


class Mutation(graphene.ObjectType):

    update_order = UpdateOrder.Field()
    create_order = CreateOrder.Field()
    create_player = CreatePlayer.Field()
    create_room = CreateRoom.Field()
    create_turn = CreateTurn.Field()
    create_unit = CreateUnit.Field()
    initilize_room = InitialRoom.Field()

