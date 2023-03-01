import graphene
from room.models.tables import Turn as TurnTable
from room.models.tables import Order as OrderTable
from room.models.tables import Outcome as OutcomeTable
from .items.turn_type import TurnType
from .items.order_type import OrderType, UpdateOrders
from .items.outcome_type import OutcomeType


class Query(graphene.ObjectType):
    turns = graphene.List(TurnType)
    order = graphene.List(OrderType, order_id=graphene.Int())
    outcome = graphene.List(OutcomeType)
    
    def resolve_last_turn(root):
        # Querying for unit
        return TurnTable.objects.last()

    def resolve_all_orders(root):
        # Querying for unit
        return OrderTable.objects.all()

    def resolve_one_orders(root, turn):
        # Querying for unit
        return OrderTable.objects.filter(turn=turn).all()
    
    def resolve_all_outcomes(root):
        # Querying for unit
        return OutcomeTable.objects.all()

class Mutation(graphene.ObjectType):
    
    update_order = UpdateOrders.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)