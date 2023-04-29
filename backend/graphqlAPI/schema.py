import graphene
# from room.models.locations import Map, Country, Location
# from django.contrib.auth.models import User
# from room.models.order import Turn, Order, Outcome
# from room.game.unitTypes import Unit
# from host.models.player import Player
# from .items.table_type import *
from .items.order_mutation import UpdateOrder
from .items.user_mutaionn import CreateUserMutation
from room .schema import Query as room_query


class Query(room_query, graphene.ObjectType):
    # turns = graphene.List(TurnType)
    # units = graphene.List(UnitType)
    # orders = graphene.List(OrderType, order_id=graphene.Int())
    # outcomes = graphene.List(OutcomeType)
    # locations = graphene.List(LocationType)
    # map = graphene.List(MapType)
    # country = graphene.List(CountryType)
    # map_polygon = graphene.List(Map_PolygonType)
    # next_to = graphene.List(Next_toType)
    # player = graphene.List(PlayerType)
    # user = graphene.List(UserType)
    # """
    # A Resolver is a method that helps us answer Queries by fetching data for a Field in our Schema.
    # Resolvers are lazily executed, so if a field is not included in a query, its resolver will not be executed.
    # Each field on an ObjectType in Graphene should have a corresponding resolver method to fetch data.
    # """
    # def resolve_turns(root, info, **kwargs):
    #     return Turn.objects.all()
    
    # def resolve_units(root, info, **kwargs):
    #     return Unit.objects.all()

    # def resolve_orders(root, info, **kwargs):
    #     return Order.objects.all()
    
    # def resolve_outcomes(root, info, **kwargs):
    #     return Outcome.objects.all()
    
    # def resolve_locations(root, info, **kwargs):
    #     return Location.objects.all()

    # def resolve_map(root, info, **kwargs):
    #     return Map.objects.all()

    # def resolve_map_polygon(root, info, **kwargs):
    #     return Map_Polygon.objects.all()

    # def resolve_next_to(root, info, **kwargs):
    #     return Next_to.objects.all()

    # def resolve_country(root, info, **kwargs):
    #     return Country.objects.all()
    
    # def resolve_player(root, info, **kwargs):
    #     return Player.objects.all()
    
    # def resolve_user(root, info, **kwargs):
    #     return User.objects.all()
        from django.conf import settings
        from graphene_django.debug import DjangoDebug
        if settings.DEBUG:
         # Debug output - see
         # http://docs.graphene-python.org/projects/django/en/latest/debug/
            # debug = graphene.Field(DjangoDebug, name='__debug')
            pass
        


class Mutation(graphene.ObjectType):
    
    update_order = UpdateOrder.Field()
    create_user = CreateUserMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)