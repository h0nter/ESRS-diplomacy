from host.models import Host
import step

class Playing(step.Step):

    @classmethod
    def main(cls):
        def __init__(host:classmethod):
            cls.host = host
            cls.StatusType = host.room_status
            cls.initialize()

        cls.host(room_status='Open').save()
        
        while cls.StatusType == 'Opening':
            # waiting process
            is_opening = cls.opening()
            if is_opening != True:
                cls.StatusType = 'Wait'

        while cls.StatusType != 'Closing':
        
            while cls.StatusType == 'Wait':
                # waiting process
                is_waiting = cls.waiting()
                if is_waiting != True:
                   cls.StatusType = 'Check'
            
            while cls.StatusType == 'Check':
                # Checking the closeing conditions
                is_finish = cls.checking()
                if is_finish:
                    cls.StatusType = 'Closing'
                else:
                    cls.StatusType = 'Check'


        cls.Closing() 