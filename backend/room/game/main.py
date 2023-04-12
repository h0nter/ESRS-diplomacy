from step import Step


class Room(Step):
    def __init__(cls, host: object):
        super().__init__(host)

    @classmethod
    def launch(cls) -> None:        
        while cls.StatusType != 'Closed': # while the game is not closed, execute the following step
        
            if cls.StatusType == 'Opening': # open the room and wait for player to join in
                cls.opening()
                
            elif cls.StatusType == 'Waiting': # wait for user to commit their order
                cls.waiting()

            elif cls.StatusType == 'Checking': # Check the closeing conditions
                cls.checking()

            elif cls.StatusType == 'ending':  # the status before the room are totaly closed.
                cls.ending()

        cls.closed()
