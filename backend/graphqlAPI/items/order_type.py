from graphene_django import DjangoObjectType
from ...room.models.tables import Order
import graphene


class OrderType(DjangoObjectType):
    class Meta: 
        model = Order
        fields = "__all__"


# ------------prepare for the mutation------------
# class UpdateOrders(graphene.Mutation):
#     class Arguments:
#         # Mutation to update a unit 
#         
#     order = graphene.Field(OrderType)

#     @classmethod
#     def mutate(cls, order, turn, target_unit, current_location, reference_unit, reference_unit_current_location, reference_unit_new_location):

#         return OrderType(order=order)

class CreateOrders(graphene.Mutation):
    class Arguments:
        # Mutation to create a unit
        order = graphene.String(required=True)

    # Class attributes define the response of the mutation
    unit = graphene.Field(OrderType)

    @classmethod
    def mutate(cls, belong, position, can_float):
        order = Order()
        order.belong = belong
        order.position = position
        order.can_float = can_float
        order.save()
        
        return CreateOrders(order = order)