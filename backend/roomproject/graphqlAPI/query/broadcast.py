import graphene
from .table_type import *
from room.models.order import Turn, Order
from room.models.player import Player
from room.models.room import Room
from room.models.broadcast import OrderBroadcast


class GameAPI(graphene.ObjectType):

    turn = graphene.List(TurnType, room_id=graphene.Int())
    room = graphene.List(RoomType, player_id=graphene.Int())
    player = graphene.List(PlayerType, user_id=graphene.Int())
    order = graphene.List(OrderType, order_id=graphene.Int())
    OrderBroadcast = graphene.List(OrderBroadcastType, turn_id=graphene.Int(), room_id=graphene.Int(), unit_id=graphene.Int())
    
    """
    A Resolver is a method that helps us answer Queries by fetching data for a Field in our Schema.
    Resolvers are lazily executed, so if a field is not included in a query, its resolver will not be executed.
    Each field on an ObjectType in Graphene should have a corresponding resolver method to fetch data.
    """
    
    def resolve_turn(root, info, **kwargs):
        room_id = kwargs.get('room_id')
        if room_id != None:
            turn_id = Room.objects.get(pk=room_id).current_turn
            return Turn.objects.filter(pk=turn_id)
        
        return Turn.objects.all()

    def resolve_room(root, info, **kwargs):
        player_id = kwargs.get('player_id')
        if player_id != None:
            room_id = Player.objects.get(pk=player_id).room.id
            return  Room.objects.filter(pk=room_id)
            
        return Room.objects.all()

    def resolve_player(root, info, **kwargs):
        user_id = kwargs.get('user_id')
        if user_id != None:
            return  Player.objects.filter(user_id=user_id)
            
        return Player.objects.all()

    def resolve_order(root, info, **kwargs):
        if kwargs.get('order_id'):
            return Order.objects.filter(pk=kwargs.get('order_id'))
        else:
            return Order.objects.all()
        
    def resolve_OrderBroadcast(root, info, **kwargs):
        if len(kwargs.keys()) != 0:
            turn_id = kwargs.get('turn_id')
            room_id = kwargs.get('room_id')
            unit_id = kwargs.get('unit_id')
            return OrderBroadcast.objects.filter(room__id=room_id, order__turn__id=turn_id, order__unit_id=unit_id)
        else:
            return OrderBroadcast.objects.all()