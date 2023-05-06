class Step:
    def __init__(cls, host:object):
            cls.host = host
            cls.StatusType = host.room_status
            cls.initialize()
            
    @classmethod
    def isFinished() -> bool:
         pass

    @classmethod
    def initialize(cls) -> None: # format the room database
        cls.host(room_status='Open').save()

    @classmethod
    def opening(cls) -> None: # wait for user to login the game.
        cls.host(room_status='Wait').save()
        
    @classmethod
    def waiting(cls) -> None: # wait for user to make a decision
        cls.host(room_status='Check').save()

    @classmethod
    def checking(cls) -> None: # need to update the status to host app
        if cls.isFinished():
            cls.host(room_status='end').save()

    @classmethod
    def ending(cls) -> None: # the status before the room are totaly closed.
        cls.host(room_status='close').save()
    
    @classmethod
    def closed(cls) -> None: # will only change the status to be 'closed'
        cls.host(room_status='closed').save()