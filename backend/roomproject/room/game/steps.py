from room.game.legitamiseOrders import LegitamiseOrders
from room.game.resolveOrders import ResolveOrders
from room.models.broadcast import Room, RoomStatus
from room.models.order import Outcome
from django.core.management import call_command

class Step:
    @classmethod
    def __init__(cls, room_ID:int):
            cls.room = Room.objects.get(pk=room_ID)
            cls.status = cls.room.room_status
            cls.current_turn = cls.room.current_turn
            if cls.status == RoomStatus.INITIAL: # Formating the room database
                cls.initialize()
                # sets RoomStatus to OPEN
    
    @classmethod
    def room_factory(cls, room_id):
        return cls(room_id)
            
    @classmethod
    def isFinished(cls) -> bool:
        return True
    
    @staticmethod
    def create_turn():
        pass

    @classmethod
    def initialize(cls) -> None: # format the room database
        call_command('loaddata', 'room/fixtures/*json')
        cls.room.status = RoomStatus.OPEN
        cls.room.save()

    @classmethod
    def opening(cls) -> None: # wait for user to login the game.
        cls.room.status = RoomStatus.WAITING
        cls.room.save()
        
    @classmethod
    def waiting(cls) -> None: # wait for user to make a decision

        # Check time, if past time go to resolve
        cls.room.status = RoomStatus.RESOLVE
        cls.room.save()

    @classmethod
    def resolve(cls) -> None: # resolve orders
        LegitamiseOrders(cls.current_turn)
        ResolveOrders(cls.current_turn)
        if len(Outcome.objects.get_outcomes_retreat(cls.current_turn)) > 1:
            # increase to sub-turn
            # set all orders for this turn to hold bar the retreaters

            cls.room.status = RoomStatus.RETREAT
            cls.room.save()
        else:
            cls.room.status = RoomStatus.UPDATE
            cls.room.save()

    @classmethod
    def retreat(cls) -> None: # wait for user to make a decision on retreats

        # check time, if past time go to resolve 
        cls.room.status = RoomStatus.RESOLVE
        cls.room.save()

    @classmethod
    def update(cls) -> None: # Update map with new Unit Positions

        # update unit positions

        if cls.current_turn.is_autumn:
            cls.room.status = RoomStatus.RESUPPLY
            cls.room.save()
        else:
            cls.room.status = RoomStatus.CHECKING
            cls.room.save()

    @classmethod
    def resupply(cls) -> None: # Gaining Units After FALL
        
        # wait for user input on new unit location
        # or random?

        cls.room.status = RoomStatus.CHECKING
        cls.room.save()

    @classmethod
    def checking(cls) -> None: # need to update the status to room app
        # increase turn here!
        
        if cls.isFinished():
            cls.room.status = RoomStatus.CLOSED
            cls.room.save()
        else:
            cls.room.status = RoomStatus.WAITING
            cls.room.save()
