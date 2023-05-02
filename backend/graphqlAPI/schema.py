import graphene
from .items.table_type import *
from .items.user_mutaionn import CreateUserMutation
from .items.host_mutation import CreateHostMutation
from room.schema import Query as room_query
from room.schema import Mutation as room_mutation
from host.models.host import Host


class Query(room_query, graphene.ObjectType):

    room = graphene.List(HostType)
    user = graphene.List(UserType)
    # player = graphene.List(PlayerType)

    """
    A Resolver is a method that helps us answer Queries by fetching data for a Field in our Schema.
    Resolvers are lazily executed, so if a field is not included in a query, its resolver will not be executed.
    Each field on an ObjectType in Graphene should have a corresponding resolver method to fetch data.
    # """
    def resolve_host(root, info, **kwargs):
        return Host.objects.all()
    
    # def resolve_player(root, info, **kwargs):
    #     return Player.objects.all()
    
    def resolve_user(root, info, **kwargs):
        return User.objects.all()


class Mutation(room_mutation, graphene.ObjectType):
    
    create_user = CreateUserMutation.Field()
    create_room = CreateHostMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)