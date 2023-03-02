import graphene
from room.tables import Turn, Unit, Order, Outcome,Location
from .items.table_type import TurnType, UnitType, OrderType, OutcomeType, LocationType
from .items.order_mutation import UpdateOrder


class Query(graphene.ObjectType):
    turns = graphene.List(TurnType)
    units = graphene.List(UnitType)
    orders = graphene.List(OrderType, order_id=graphene.Int())
    outcome = graphene.List(OutcomeType)
    locations = graphene.List(LocationType)

    # A Resolver is a method that helps us answer Queries by fetching data for a Field in our Schema.
    # Resolvers are lazily executed, so if a field is not included in a query, its resolver will not be executed.
    # Each field on an ObjectType in Graphene should have a corresponding resolver method to fetch data.
    def resolve_turns(root, info, **kwargs):
        return Turn.objects.all()
    
    def resolve_units(root, info, **kwargs):
        return Unit.objects.all()

    def resolve_orders(root, info, **kwargs):
        return Order.objects.all()
    
    def resolve_outcomes(root):
        return Outcome.objects.all()
    
    def resolve_locations(root):
        return Location.objects.all()

class Mutation(graphene.ObjectType):
    
    update_order = UpdateOrder.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)