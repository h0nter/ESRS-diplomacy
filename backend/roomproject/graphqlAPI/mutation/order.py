import graphene
from room.models.location import Location
from room.models.room import Room
from room.models.order import Turn, Order, Unit, MoveType
from graphqlAPI.query.table_type import OrderType


# prepare a input arguments
class OrderInput(graphene.InputObjectType):
    # basic information, disable to be null
    room_id = graphene.ID(required=True)
    instruction = graphene.String(required=True)
    turn_id = graphene.ID(required=True)
    unit_id = graphene.ID(required=True)
    # move operation
    target_location_id = graphene.ID() 
    # convoy operation only
    reference_unit_id = graphene.ID()
    reference_unit_current_location_id = graphene.ID()
    reference_unit_new_location_id = graphene.ID()

class UpdateOrder(graphene.Mutation):
    # reference from class OrderInput
    class Arguments:
        input = OrderInput(required=True)
    
    ok = graphene.Boolean() 
    order = graphene.Field(OrderType)
    
    # Mutation to update a unit 
    @classmethod
    def mutate(cls, root, info, input, id=None):

        order = Order.objects.get(room__id=input.room_id,
                                            turn__id=input.turn_id,
                                            unit__id=input.unit_id)

        order.instruction = input.instruction
        # order.turn = Turn.objects.get(pk=input.turn_id)
        # order.unit = Unit.objects.get(pk=input.unit_id)
        # while instruction is Convoy, allow further info to be stored.
        if order.instruction == MoveType.CONVOY or order.instruction == MoveType.SUPPORT:
            order.reference_unit = Unit.objects.get(pk=input.reference_unit_id)
            order.reference_unit_current_location = Location.objects.get(pk=input.reference_unit_current_location_id)
            order.reference_unit_new_location = Location.objects.get(pk=input.reference_unit_new_location_id)

        order.save()

        return UpdateOrder(ok=True, order=order)
    

class CreateOrder(graphene.Mutation):
    # reference from class OrderInput
    class Arguments:
        input = OrderInput(required=True)
    
    order = graphene.Field(OrderType)
    
    # Mutation to update a unit 
    @classmethod
    def mutate(cls, root, info, input, id=None):
        turn = Turn.objects.get(pk=input.turn_id)
        room = Room.objects.get(pk=input.room_id)
        if turn == None:
            turn = Turn.objects.create(year=room.current_turn)

        order = Order.objects.create(
                                    instruction = input.instruction,
                                    turn = Turn.objects.create(pk=input.turn_id),
                                    target_unit = Unit.objects.get(pk=input.unit_id))
        
        if order.instruction == MoveType.MOVE:
            order.target_location = Location.objects.get(pk=input.target_location_id)
        
        # while instruction is Convoy, allow further info to be stored.
        if order.instruction == MoveType.CONVOY or order.instruction == MoveType.SUPPORT:
            order.reference_unit = Unit.objects.get(pk=input.reference_unit_id)
            order.reference_unit_current_location = Location.objects.get(pk=input.reference_unit_current_location_id)
            order.reference_unit_new_location = Location.objects.get(pk=input.reference_unit_new_location_id)
        
        order.save()

        return UpdateOrder(ok=True, order=order)