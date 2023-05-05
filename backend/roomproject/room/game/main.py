from .steps import Step
from ..models.room import Room


class Game(Step):
    def __init__(cls, room_name:str):
            cls.room = Room.objects.get(room_name=room_name)
            cls.status = cls.room.room_status
    
    @classmethod
    def factory(cls, room_name):
        return cls(room_name)

    @classmethod
    def start(cls) -> None:

        while cls.status != 'Closed': # while the game is not closed, execute the following step
            if cls.status == 'initial': # wait for user to commit their order
                cls.initialize()
           
            elif cls.status == 'Waiting': # wait for user to commit their order
                cls.waiting()

            elif cls.status == 'Checking': # Check the closeing conditions
                cls.checking()

            elif cls.status == 'ending':  # the status before the room are totaly closed.
                cls.ending()

        # cls.closed()
        print('class',__class__.__name__,'had called.')

