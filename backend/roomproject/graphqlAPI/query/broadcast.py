import graphene
from .table_type import *
from room.models.order import Turn, Order
from room.models.player import Player
from room.models.room import Room
from room.models.broadcast import OrderBroadcast


class GameAPI(graphene.ObjectType):

    turn = graphene.List(TurnType, player_id=graphene.Int())
    room = graphene.List(RoomType, user_id=graphene.Int())
    player = graphene.List(PlayerType, user_id=graphene.Int())
    order = graphene.List(OrderType, order_id=graphene.Int(), unit_id=graphene.Int())
    
    """
    A Resolver is a method that helps us answer Queries by fetching data for a Field in our Schema.
    Resolvers are lazily executed, so if a field is not included in a query, its resolver will not be executed.
    Each field on an ObjectType in Graphene should have a corresponding resolver method to fetch data.
    """
    
    def resolve_turn(root, info, **kwargs):
        if kwargs.items != None:
            try:
                return Room.objects.get(pk=kwargs.get('room_id')).current_turn
            except:
                return "incorrect input parameter"

        return Turn.objects.all()

    def resolve_room(root, info, **kwargs):
        if kwargs.items != None:
            try: 
                return {"rooms": [x.room for x in Player.objects.filter(pk=kwargs.get('player_id'))]}
            except:
                return "incorrect input parameter"
            
        return Room.objects.all()

    def resolve_player(root, info, **kwargs):
        if kwargs.items != None:
            try: 
                return {"players": [x for x in Player.objects.filter(user_id=kwargs.get('user_id'))]}
            except:
                return "incorrect input parameter"
            
        return Player.objects.all()

    def resolve_order(root, info, **kwargs):
        if kwargs.get('order_id'):
                return Order.objects.get(pk=kwargs.get('order_id'))
        else:
            unit_id = kwargs.get('unit_id')
            turn_id = kwargs.get('turn_id')
            room_id = kwargs.get('room_id')
            return OrderBroadcast.objects.get(order__target_unit__pk=unit_id, turn__pk=turn_id, room__pk=room_id)
        