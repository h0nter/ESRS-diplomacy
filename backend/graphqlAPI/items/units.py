import graphene
from graphene_django import DjangoObjectType
from ...room.models.tables import Units

class UnitsType(DjangoObjectType):
    class Meta: 
        model = Units
        fields = ('id', 'belong', 'position', 'can_float')

class UpdateUnits(graphene.Mutation):
    class Arguments:
        # Mutation to update a unit 
        id = graphene.ID()
        belong = graphene.String(required=True)
        position = graphene.String(required=True)
        can_float = graphene.Boolean()
        
    unit = graphene.Field(UnitsType)

    @classmethod
    def mutate(cls, root, info, name, id):
        unit = Units.objects.get(pk=id)
        unit.id = id
        unit.save()
        
        return UpdateUnits(unit=unit)

class CreateUnits(graphene.Mutation):
    class Arguments:
        # Mutation to create a unit
        name = graphene.String(required=True)

    # Class attributes define the response of the mutation
    unit = graphene.Field(UnitsType)

    @classmethod
    def mutate(cls, root, info, belong, position, can_float):
        unit = Units()
        unit.belong = belong
        unit.position = position
        unit.can_float = can_float
        unit.save()
        
        return CreateUnits(unit = unit)