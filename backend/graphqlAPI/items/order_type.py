import graphene
from graphene_django import DjangoObjectType
from room.models.tables import Order


class OrderType(DjangoObjectType):
    class Meta: 
        model = Order
        fields = "__all__"

# prepare a input arguments
class OrderInput(graphene.InputObjectType):
    # basic information, disable to be null
    instruction = graphene.String(required=True)
    year = graphene.Int(required=True)
    can_float = graphene.Boolean(required=True)
    target_unit = graphene.String(required=True)
    current_location = graphene.String(required=True)
    # convoy operation only
    reference_unit_pk = graphene.Int()
    reference_unit_current_location_pk = graphene.Int()
    reference_unit_new_location_pk = graphene.Int()

class UpdateOrders(graphene.Mutation):
    # reference from class OrderInput
    class Arguments:
        input = OrderInput(required=True)
    
    ok = graphene.Boolean()

    # Mutation to update a unit 
    @classmethod
    def mutate(cls, root, info, input):
        order = Order()
        order.instruction = input.instruction
        
        return OrderType(ok=True)