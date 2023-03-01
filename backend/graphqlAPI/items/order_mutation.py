import graphene
from graphene_django import DjangoObjectType
from room.models.tables import Order, Turn, Unit, Location
from .table_type import OrderType


# prepare a input arguments
class OrderInput(graphene.InputObjectType):
    # basic information, disable to be null
    instruction = graphene.String(required=True)
    turn = graphene.Int(required=True)
    target_unit = graphene.Int(required=True)
    current_location = graphene.Int(required=True)
    # convoy operation only
    reference_unit_pk = graphene.Int()
    reference_unit_current_location_pk = graphene.Int()
    reference_unit_new_location_pk = graphene.Int()

class UpdateOrder(graphene.Mutation):
    # reference from class OrderInput
    class Arguments:
        input = OrderInput(required=True)
    
    
    order = graphene.Field(OrderType)

    # Mutation to update a unit 
    @classmethod
    def mutate(cls, root, info, input):
        order = Order()
        order.instruction = input.instruction
        order.turn = Turn.objects.get(pk=input.turn)
        order.target_unit = Unit.objects.get(pk=input.target_unit)
        order.current_location = Location.objects.get(pk=input.current_location)
        
        order.save()
        print('succesful save')

        return UpdateOrder(oder=order)