import graphene
from .items.table_type import *
from .items.user_mutaionn import CreateUserMutation
from .items.room_mutation import CreateRoomMutation
from room.schema import Query as room_query
from room.schema import Mutation as room_mutation
from host.models.room import Room


class Query(room_query, graphene.ObjectType):

    room = graphene.List(RoomType)
    user = graphene.List(UserType)
    player = graphene.List(PlayerType)

    """
    A Resolver is a method that helps us answer Queries by fetching data for a Field in our Schema.
    Resolvers are lazily executed, so if a field is not included in a query, its resolver will not be executed.
    Each field on an ObjectType in Graphene should have a corresponding resolver method to fetch data.
    # """
    def resolve_room(root, info, **kwargs):
        return Room.objects.all()
    
    def resolve_player(root, info, **kwargs):
        return Player.objects.all()
    
    def resolve_user(root, info, **kwargs):
        return User.objects.all()


class Mutation(room_mutation, graphene.ObjectType):
    
    create_user = CreateUserMutation.Field()
    create_room = CreateRoomMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)