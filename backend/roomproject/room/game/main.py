from room.game.steps import Step
from room.models.room import Room, RoomStatus



class Game(Step):

    @classmethod
    def __init__(cls, room_id: int):
        cls.room = Room.objects.get(pk=room_id)
        cls.status = cls.room.room_status
        if cls.status == RoomStatus.INITIAL:  # Formating the room database
            cls.initialize()
            # sets RoomStatus to OPEN
    
    @classmethod
    def factory(cls, room_name):
        return cls(room_name)

    @classmethod
    # SHOULD THIS BE asynchronous? Only called when triggered from frontend?
    def start(cls) -> None:

        # while the game is not closed, execute the following step
        while cls.status != RoomStatus.CLOSED: 
            
            if cls.status == RoomStatus.WAITING: 
                # wait for user to commit their order
                cls.waiting()
            elif cls.status == RoomStatus.RESOLVE:
                # resolve the committed orders
                cls.resolve()
            elif cls.status == RoomStatus.RETREAT:
                # orders incoming again but only retreats
                # set as a sub turn?
                cls.retreat()
            elif cls.status == RoomStatus.UPDATE:
                # Update map with new unit positions
                cls.update()
            elif cls.status == RoomStatus.RESUPPLY:
                # IF it's Autumn, add in new units at resupply points
                cls.resupply()
            elif cls.status == RoomStatus.CHECKING:
                # Check the closeing conditions -> sets to ClOSED
                cls.checking()

        # cls.closed()
        print('class',__class__.__name__,'had called.')

