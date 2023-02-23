from graphene_django import DjangoObjectType
from ...room.models.tables import Unit


class UnitType(DjangoObjectType):
    class Meta: 
        model = Unit
        fields = "__all__"
