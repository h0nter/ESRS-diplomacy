from room.game.legitamiseOrders import LegitamiseOrders
from room.game.resolveOrders import ResolveOrders
from room.models.room import RoomStatus, Room
from room.models.order import Order, MoveType
from room.models.outcome import Outcome
from room.models.turn import Turn
from room.models.unit import Unit
from room.models.location_owner import LocationOwner
from django.core.management import call_command
import json
import datetime

class Step:
    @classmethod
    def __init__(cls, room_id: int):
        cls.room = Room.objects.get(pk=room_id)
        cls.status = cls.room.status
        cls.map = cls.room.map
        if cls.status == RoomStatus.REGISTERED:  # Formating the room database
            cls.initialize()
            # sets RoomStatus to OPEN

    # @classmethod
    # def room_factory(cls, room_id):
    #     return cls(room_id)

    @classmethod
    def isFinished(cls) -> bool:
        return cls.current_turn.year > 1950
    
    @classmethod
    def initializeUnits(cls):
        with open('./data/unit.json','r',encoding='utf-8') as j:
            units = json.loads(j.read())
        units = units[cls.map]
        for unit in units:
            unitModel = Unit(
                owner=unit['unit_owner'],
                room=cls.room,
                location=unit['unit_location'],
                can_float=unit['unit_can_float']
            )
            unitModel.save()

    @classmethod
    def initializeLocationOwners(cls):
        with open('./data/location_owner.json','r',encoding='utf-8') as j:
            location_owners = json.loads(j.read())
        location_owners = location_owners[cls.map]
        for location_owner in location_owners:
            location_ownerModel = LocationOwner(
                current_owner=location_owner['country_pk'],
                room=cls.room,
                location=location_owner['location_pk'],
            )
            location_ownerModel.save()
            

    @classmethod
    def initializeTurnOrders(cls):
        for unit in Unit.objects.all():
            order = Order(instruction=MoveType.HOLD,
                          turn=cls.current_turn,
                          target_unit=unit,
                          current_location=unit.location)
            order.save()

    @classmethod
    def initialize(cls) -> None:  
        # format the room database
        call_command('loaddata', 'room/fixtures/*json')
        cls.initializeLocationOwners()
        cls.initializeUnits()

        # set first turn
        cls.room.current_turn = Turn.objects.get(year=1901, is_autumn=False)
        cls.current_turn = cls.room.current_turn
        cls.initializeTurnOrders()

        cls.room.status = RoomStatus.WAITING
        cls.room.save()

    @classmethod
    def waiting(cls) -> None:  # wait for user to make a decision
        if cls.room.close_time is None:
            cls.room.set_close_time()
        elif cls.room.close_time <= datetime.datetime.now():
            # Check time, if past time go to resolve
            cls.room.status = RoomStatus.RESOLVE
            cls.room.save()

    @classmethod
    def resolve(cls) -> None:  # resolve orders
        LegitamiseOrders(cls.current_turn,cls.room)
        ResolveOrders(cls.current_turn,cls.room)
        # if some need to retreat
        retreaters = Outcome.objects.get_outcomes_retreat(cls.current_turn,cls.room)
        if len(retreaters) > 1:
            # increase to sub-turn
            if cls.current_turn.is_autumn:
                turn = Turn(year=cls.current_turn.year,
                            is_autumn=True, is_retreat_turn=True)
                turn.save()
            else:
                turn = Turn(year=cls.current_turn.year, is_retreat_turn=True)
                turn.save()
            cls.current_turn = turn
            # set all orders for this turn to hold
            cls.initializeTurnOrders()
            # send the retreaters to front end??

            cls.room.status = RoomStatus.RETREAT
            cls.room.save()
        else:
            cls.room.status = RoomStatus.UPDATE
            cls.room.save()

    @classmethod
    def retreat(cls) -> None:  # wait for user to make a decision on retreats
        if cls.room.close_time is None:
            cls.room.set_close_time()
        elif cls.room.close_time <= datetime.datetime.now():
            # check time, if past time go to resolve
            cls.room.status = RoomStatus.RESOLVE
            cls.room.save()

    @classmethod
    def update(cls) -> None:  # Update map with new Unit Positions
        # set temp retreat turn to different var
        retreat_turn = cls.current_turn
        # get turn from start of 'turn'
        cls.current_turn = Turn.objects.get(year=retreat_turn.year,
                                            is_autumn=retreat_turn.is_autumn,
                                            is_retreat_turn=False)
        # update unit positions
        Outcome.objects.perform_move_operations(retreat_turn,cls.room)
        Outcome.objects.perform_move_operations(cls.current_turn,cls.room)

        if cls.current_turn.is_autumn:
            cls.room.status = RoomStatus.RESUPPLY
            cls.room.save()
        else:
            cls.room.status = RoomStatus.CHECKING
            cls.room.save()

    @classmethod
    # TO-DO!
    def resupply(cls) -> None:  # Gaining Units After FALL

        # wait for user input on new unit location
        # or random?

        cls.room.status = RoomStatus.CHECKING
        cls.room.save()

    @classmethod
    def checking(cls) -> None:  # need to update the status to room app
        if cls.isFinished():
            cls.room.status = RoomStatus.CLOSED
            cls.room.save()
        else:
            # increase turn here!
            if cls.current_turn.is_autumn:
                turn = Turn(year=cls.current_turn.year+1)
                turn.save()
            else:
                turn = Turn(year=cls.current_turn.year, is_autumn=True)
                turn.save()
            cls.room.current_turn = cls.current_turn = turn
            cls.initializeTurnOrders()
            cls.room.status = RoomStatus.WAITING
            cls.room.save()
