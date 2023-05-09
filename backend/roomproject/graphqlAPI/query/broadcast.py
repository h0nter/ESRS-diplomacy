import graphene
from .table_type import *
from room.models.order import Order
from room.models.turn import Turn
from room.models.player import Player
from room.models.room import Room



class Broadcast(graphene.ObjectType):

    turn = graphene.List(TurnType, room_id=graphene.Int())
    room = graphene.List(RoomType, player_id=graphene.Int(), room_id=graphene.ID())
    player = graphene.List(PlayerType, user_id=graphene.ID(), room_id=graphene.ID())
    order = graphene.List(OrderType, turn_id=graphene.ID(), room_id=graphene.ID(), unit_id=graphene.ID())

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
            room_id = Player.objects.get(pk=player_id).room.pk
            return  Room.objects.filter(pk=room_id)

        room_id = kwargs.get('room_id')
        if room_id is not None:
            return  Room.objects.filter(pk=room_id)
            
        return Room.objects.all()

    def resolve_player(root, info, **kwargs):
        user_id = kwargs.get('user_id')
        room_id = kwargs.get('room_id')

        print('user_id', user_id)
        print('room_id', room_id)

        if user_id is not None and room_id is not None:
            return Player.objects.filter(user_id=user_id, room_id=room_id)

        if user_id is not None:
            return Player.objects.filter(user_id=user_id)

        if room_id is not None:
            return Player.objects.filter(room_id=room_id)
            
        return Player.objects.all()

    def resolve_order(root, info, **kwargs):
        if len(kwargs.keys()) != 0:
            turn_id = kwargs.get('turn_id')
            room_id = kwargs.get('room_id')
            unit_id = kwargs.get('unit_id')
            return Order.objects.filter(room__id=room_id, turn__id=turn_id, unit__id=unit_id)
        else:
            return Order.objects.all()
        
