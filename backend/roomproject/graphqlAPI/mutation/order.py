import graphene
from room.models.locations import Location
from room.models.order import Turn, Order, Unit, MoveType
from room.models.broadcast import OrderBroadcast
from graphqlAPI.query.table_type import OrderType


# prepare a input arguments
class OrderInput(graphene.InputObjectType):
    # basic information, disable to be null
    room_id = graphene.ID(required=True)
    instruction = graphene.String(required=True)
    turn_id = graphene.ID(required=True)
    unit_id = graphene.ID(required=True)
    current_location = graphene.ID(required=True)
    # convoy operation only
    reference_unit_id = graphene.ID()
    reference_unit_current_location_id = graphene.ID()
    reference_unit_new_location_id = graphene.ID()

class UpdateOrder(graphene.Mutation):
    # reference from class OrderInput
    class Arguments:
        input = OrderInput(required=True)
        id = graphene.ID()
    
    ok = graphene.Boolean() 
    order = graphene.Field(OrderType)
    
    # Mutation to update a unit 
    @classmethod
    def mutate(cls, root, info, input, id=None):
        if id:
            order = Order.objects.get(pk=id)
        else:
            order = OrderBroadcast.objects.get(room__id=input.room_id,
                                               order__turn__id=input.turn_id,
                                               order__target_unit__id=input.unit_id).order

        order.instruction = input.instruction
        order.turn = Turn.objects.get(pk=input.turn_id)
        order.target_unit = Unit.objects.get(pk=input.unit_id)
        order.current_location = Location.objects.get(pk=input.current_location)
        # while instruction is Convoy, allow further info to be stored.
        if order.instruction == MoveType.CONVOY:
            order.reference_unit = Unit.objects.get(pk=input.reference_unit_id)
            order.reference_unit_current_location = Location.objects.get(pk=input.reference_unit_current_location_id)
            order.reference_unit_new_location = Location.objects.get(pk=input.reference_unit_new_location_id)
        
        order.save()

        return UpdateOrder(ok=True, order=order)