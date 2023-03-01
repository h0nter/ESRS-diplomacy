from graphene_django import DjangoObjectType
from room.models.tables import Turn


class TurnType(DjangoObjectType):
    class Meta: 
        model = Turn
        fields = "__all__"
