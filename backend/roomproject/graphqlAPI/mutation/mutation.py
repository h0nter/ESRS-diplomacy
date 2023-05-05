import graphene
from .order_mutation import UpdateOrder

class Mutation(graphene.ObjectType):

    update_order = UpdateOrder.Field()