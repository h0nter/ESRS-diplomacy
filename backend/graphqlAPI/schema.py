import graphene
from ..room.models.tables import Unit as UnitTable
from ..room.models.tables import Order as OrderTable
from items.unit_type import UnitType
from items.order_type import OrderType, CreateOrders



class Query(graphene.ObjectType):
    units = graphene.List(UnitType)
    order = graphene.List(OrderType, order_id=graphene.Int())

    def resolve_units(root):
            # Querying for unit
            return UnitTable.objects.all()

    def resolve_all_orders(root):
            # Querying for unit
            return OrderTable.objects.all()

    def resolve_turn_orders(root, turn):
            # Querying for unit
            return OrderTable.objects.filter(turn=turn).all()


class Mutation(graphene.ObjectType):
    
    create_order = CreateOrders.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)