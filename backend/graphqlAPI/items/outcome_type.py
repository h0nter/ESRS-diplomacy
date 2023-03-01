from graphene_django import DjangoObjectType
from room.models.tables import Outcome


class OutcomeType(DjangoObjectType):
    class Meta: 
        model = Outcome
        fields = "__all__"
