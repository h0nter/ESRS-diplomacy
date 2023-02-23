import graphene
from graphene_django import DjangoObjectType
from .models.graph_demo import Category
from .models.tables import Units, Location


class UnitsType(DjangoObjectType):
    class Meta: 
        model = Units
        fields = ('id', 'belong', 'position', 'can_float')

class LocationType(DjangoObjectType):
    class Meta: 
        model = Location
        fields = ('id', 'name', 'is_sea')

class UpdateLocation(graphene.Mutation):
    class Arguments:
        # Mutation to update a category 
        name = graphene.String(required=True)
        is_sea = graphene.Boolean()
        id = graphene.ID()

    category = graphene.Field(LocationType)

    @classmethod
    def mutate(cls, root, info, name, id):
        category = Location.objects.get(pk=id)
        category.title = name
        category.save()
        
        return UpdateLocation(category=category)

class CreateLocation(graphene.Mutation):
    class Arguments:
        # Mutation to create a category
        name = graphene.String(required=True)

    # Class attributes define the response of the mutation
    location = graphene.Field(LocationType)

    @classmethod
    def mutate(cls, root, info, name, is_sea):
        location = Location()
        location.name = name
        location.is_sea = is_sea
        location.save()
        
        return CreateCategory(location = location)

class CategoryType(DjangoObjectType):
    class Meta: 
        model = Category
        fields = ('id','title')

class UpdateCategory(graphene.Mutation):
    class Arguments:
        # Mutation to update a category 
        title = graphene.String(required=True)
        id = graphene.ID()

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, title, id):
        category = Category.objects.get(pk=id)
        category.title = title
        category.save()
        
        return UpdateCategory(category=category)

class CreateCategory(graphene.Mutation):
    class Arguments:
        # Mutation to create a category
        title = graphene.String(required=True)

    # Class attributes define the response of the mutation
    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, title):
        category = Category()
        category.title = title
        category.save()
        
        return CreateCategory(category=category)

class Query(graphene.ObjectType):
    locations = graphene.List(LocationType)
    units = graphene.List(UnitsType)
    categories = graphene.List(CategoryType)

    def resolve_locations(root, info, **kwargs):
            # Querying a list
            return Location.objects.all()

    def resolve_units(root, info, **kwargs):
            # Querying a list
            return Units.objects.all()

    def resolve_categories(root, info, **kwargs):
        # Querying a list
        return Category.objects.all()

class Mutation(graphene.ObjectType):
    update_category = UpdateCategory.Field()
    create_category = CreateCategory.Field()
    update_location = UpdateLocation.Field()
    create_location = CreateLocation.Field()
        
schema = graphene.Schema(query=Query, mutation=Mutation)