import graphene
from graphene import Mutation, String
from graphqlAPI.query.table_type import RoomType
from room.models.room import Room

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
