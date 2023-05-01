from .steps import Step


class Game(Step):
    def __init__(cls, room_ID: int):
        super().__init__(room_ID)

    @classmethod
    def what_up(cls) -> None:        
        # while cls.status != 'Closed': # while the game is not closed, execute the following step
        
        #     if cls.status == 'Opening': # open the room and wait for player to join in
        #         cls.opening()
                
        #     elif cls.status == 'Waiting': # wait for user to commit their order
        #         cls.waiting()

        #     elif cls.status == 'Checking': # Check the closeing conditions
        #         cls.checking()

        #     elif cls.status == 'ending':  # the status before the room are totaly closed.
        #         cls.ending()

        # cls.closed()
        print(__class__.__name__, ' had called.')
