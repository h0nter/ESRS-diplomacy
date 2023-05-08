import graphene
from graphene import Mutation, String
from graphqlAPI.query.table_type import RoomType
from room.models.room import Room

class CreateRoom(Mutation):
    class Arguments:
        room_name = String(required=True)
    
    room = graphene.Field(RoomType)

    @staticmethod
    def mutate(root, info, room_name):
        room = Room.objects.create(room_name=room_name)
        room.save()

        return CreateRoom(room=room)
