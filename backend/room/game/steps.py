from room.game.legitamiseOrders import LegitamiseOrders
from room.game.resolveOrders import ResolveOrders
from host.models import Room
from django.core.management import call_command

class Step:
    def __init__(cls, room_ID:int):
            cls.room = Room.objects.filter(pk=room_ID)
            cls.status = cls.room.room_status
            cls.currrent_turn = cls.room.turn
            cls.last_turn
            cls.initialize()
    
    @classmethod
    def room_factory(cls, room_id):
        return cls(room_id)
            
    @classmethod
    def isFinished(cls) -> bool:
         pass
    
    @staticmethod
    def create_turn(cls):
        pass

    @classmethod
    def initialize(cls) -> None: # format the room database
        call_command('loaddata', 'room/fixtures/*json')
        cls.room.update(room_status='Open')

    @classmethod
    def opening(cls) -> None: # wait for user to login the game.
        cls.room.update(room_status='Wait')
        
    @classmethod
    def waiting(cls) -> None: # wait for user to make a decision
        cls.room.update(room_status='Check')

    @classmethod
    def checking(cls) -> None: # need to update the status to room app
        # legitamise the submitted orders
        LegitamiseOrders(turn=cls.turn)
        # resolve orders 
        ResolveOrders(turn=cls.turn)

        if cls.isFinished():
            cls.room.update(room_status='end')
        else:
            cls.room.update(room_status='Wait')

    @classmethod
    def ending(cls) -> None: # the status before the room are totaly closed.
        cls.room.update(room_status='close')
    
    @classmethod
    def closed(cls) -> None: # will only change the status to be 'closed'
        cls.room.update(room_status='closed')
