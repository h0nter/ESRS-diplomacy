import graphene
from graphene import Mutation, String, ID
from graphqlAPI.query.table_type import RoomType
from room.models.room import Room, RoomStatus

class CreateRoom(Mutation):
    class Arguments:
        room_name = String(required=True)
    
    room_name = graphene.String()
    room = graphene.Field(RoomType)

    @staticmethod
    def mutate(root, info, room_name):
        #print(isinstance(room_name,str))
        room = Room(room_name=room_name)
        room.save()
        #print('pk',room.pk)
        return CreateRoom(room_name=str(room_name),room=room)
    

class InitialRoom(Mutation):
    class Arguments:
        room_id = ID(required=True)

    
    room = graphene.Field(RoomType)

    @staticmethod
    def mutate(root, info, room_id):
        room = Room.objects.get(pk=room_id)
        room.status = RoomStatus.INITIALIZE
        room.save()
        return InitialRoom(room=room)
    
