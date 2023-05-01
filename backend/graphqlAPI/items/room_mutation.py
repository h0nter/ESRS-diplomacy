import graphene
from .table_type import RoomType
from host.models.room import Room


class CreateRoom(graphene.Mutation):
    # reference from class OrderInput
    class Arguments:
        hoster = graphene.ID()
        room_name = graphene.String()
    
    ok = graphene.Boolean() 
    room = graphene.Field(RoomType)
    
    # Mutation to update a unit 
    @classmethod
    def mutate(cls, root, info, hoster, room_name):
        room = Room.objects.create(room_name=room_name, hoster=hoster)

            
        # print('Do some verify')
        # room.save()
        # print('Saved successfully')

        return CreateRoom(ok=True, room=room)