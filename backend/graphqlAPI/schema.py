import graphene
from room.models.tables import Turn, Unit, Order, Outcome,Location
from .items.table_type import TurnType, UnitType, OrderType, OutcomeType, LocationType
from .items.order_mutation import UpdateOrders


class Query(graphene.ObjectType):
    turns = graphene.List(TurnType)
    units = graphene.List(UnitType)
    orders = graphene.List(OrderType, order_id=graphene.Int())
    outcome = graphene.List(OutcomeType)
    locations = graphene.List(LocationType)

    # A Resolver is a method that helps us answer Queries by fetching data for a Field in our Schema.
    # Resolvers are lazily executed, so if a field is not included in a query, its resolver will not be executed.
    # Each field on an ObjectType in Graphene should have a corresponding resolver method to fetch data. The resolver method should match the field name. 

    def resolve_turns(root, info, **kwargs):
        # Querying for turn
        return Turn.objects.all()
    
    def resolve_units(root, info, **kwargs):
        # Querying for all units
        return Unit.objects.all()

    def resolve_orders(root, info, **kwargs):
        # Querying for one order
        return Order.objects.all()
    
    def resolve_outcomes(root):
        # Querying for all outcomes
        return Outcome.objects.all()
    
    def resolve_locations(root):
        # Querying for all outcomes
        return Location.objects.all()

class Mutation(graphene.ObjectType):
    
    update_order = UpdateOrders.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)