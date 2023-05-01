from django.contrib.auth.models import User
from graphene_django import DjangoObjectType
from host.models.room import Room
from host.models.player import Player



# allow access overall parameters
class RoomType(DjangoObjectType):
    class Meta: 
        model = Room
        fields = "__all__"

class UserType(DjangoObjectType):
    class Meta: 
        model = User
        fields = ["username", "id", "is_staff"]

class PlayerType(DjangoObjectType):
    class Meta: 
        model = Player
        fields = "__all__"