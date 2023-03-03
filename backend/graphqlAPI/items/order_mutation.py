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
        id = graphene.ID()
    
    ok = graphene.Boolean() 
    order = graphene.Field(OrderType)
    
    # Mutation to update a unit 
    @classmethod
    def mutate(cls, root, info, input, id):
        order = Order.objects.get(pk=id)
        order.instruction = input.instruction
        order.turn = Turn.objects.get(pk=input.turn)
        order.target_unit = Unit.objects.get(pk=input.target_unit)
        order.current_location = Location.objects.get(pk=input.current_location)
        # while instruction is Convoy, allow further info to be stored.
        if order.instruction == 'CVY':
            order.reference_unit = Unit.objects.get(pk=input.reference_unit_pk)
            order.reference_unit_current_location = Location.objects.get(pk=input.reference_unit_current_location_pk)
            order.reference_unit_new_location = Location.objects.get(pk=input.reference_unit_new_location_pk)
            
        print('Do some verify')
        order.save()
        print('Saved successfully')

        return UpdateOrder(ok=True, order=order)