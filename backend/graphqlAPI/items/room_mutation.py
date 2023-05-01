import graphene
from .table_type import RoomType
from host.models.room import Room, User


class CreateRoomMutation(graphene.Mutation):
    # reference from class OrderInput
    class Arguments:
        hoster = graphene.ID()
        room_name = graphene.String()
    
    ok = graphene.Boolean() 
    room = graphene.Field(RoomType)
    
    # Mutation to update a unit 
    @classmethod
    def mutate(cls, root, info, hoster, room_name):
        room = Room.objects.create(hoster=User.objects.get(pk=hoster), room_name=room_name)
        room.save()
        return CreateRoomMutation(ok=True, room=room)
    