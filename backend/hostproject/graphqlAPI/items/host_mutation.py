import graphene
from .table_type import HostType
from host.models.host import Host


from time import sleep
from threading import Thread
 
# a custom function that blocks for a moment
def task():
    for i in range(5):
        print('this is round: ', i)
        sleep(3)
 

class CreateHostMutation(graphene.Mutation):
    # reference from class OrderInput
    class Arguments:
        hoster = graphene.ID()
        room_name = graphene.String()
    
    ok = graphene.Boolean() 
    # room = graphene.Field(HostType)
    
    # Mutation to update a unit 
    @classmethod
    def mutate(cls, root, info, hoster, room_name):
        # room = Room.objects.create(hoster=User.objects.get(pk=hoster), room_name=room_name)
        # room.save()
        
        from room.game.main import Game
        # create a thread
        thread = Thread(target=Game(room_name).start)
        # run the thread
        thread.start()

        return CreateHostMutation(ok=True)
    