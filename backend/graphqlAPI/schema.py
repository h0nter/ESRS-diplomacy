import graphene
from room.models.locations import Map, Map_Polygon, Next_to, Country, Location
from room.models.order import Turn, Order, Outcome
from room.game.unitTypes import Unit
from .items.table_type import *
from .items.order_mutation import UpdateOrder


class Query(graphene.ObjectType):
    turns = graphene.List(TurnType)
    units = graphene.List(UnitType)
    orders = graphene.List(OrderType, order_id=graphene.Int(), unit_id=graphene.Int())
    outcomes = graphene.List(OutcomeType)
    locations = graphene.List(LocationType)
    map = graphene.List(MapType)
    country = graphene.List(CountryType)
    map_polygon = graphene.List(Map_PolygonType)
    next_to = graphene.List(Next_toType)

    # A Resolver is a method that helps us answer Queries by fetching data for a Field in our Schema.
    # Resolvers are lazily executed, so if a field is not included in a query, its resolver will not be executed.
    # Each field on an ObjectType in Graphene should have a corresponding resolver method to fetch data.
    def resolve_turns(root, info, **kwargs):
        return Turn.objects.all()
    
    def resolve_units(root, info, **kwargs):
        return Unit.objects.all()

    def resolve_orders(root, info, **kwargs):
        if kwargs.get('order_id'):
            return Order.objects.filter(pk=kwargs.get('order_id'))
        if kwargs.get('unit_id'):
            return Order.objects.filter(target_unit__pk=kwargs.get('unit_id'), turn__pk=Turn.objects.last().id)
        return Order.objects.all()

    # def resolve_orders_by_unit_id(root, info, unit_id):
    #     return Order.objects.filter(unit_id=unit_id)
    
    def resolve_outcomes(root, info, **kwargs):
        return Outcome.objects.all()
    
    def resolve_locations(root, info, **kwargs):
        return Location.objects.all()

    def resolve_map(root, info, **kwargs):
        return Map.objects.all()

    def resolve_map_polygon(root, info, **kwargs):
        return Map_Polygon.objects.all()

    def resolve_next_to(root, info, **kwargs):
        return Next_to.objects.all()

    def resolve_country(root, info, **kwargs):
        return Country.objects.all()

class Mutation(graphene.ObjectType):
    
    update_order = UpdateOrder.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)