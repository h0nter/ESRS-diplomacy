import graphene
from graphene_django import DjangoObjectType
from .models.graph_demo import Category, Book, Grocery
from .models.tables import Units, Location


class UnitsType(DjangoObjectType):
    class Meta: 
        model = Units
        fields = ('id', 'belong', 'position', 'can_float')

class LocationType(DjangoObjectType):
    class Meta: 
        model = Location
        fields = ('id', 'name', 'is_sea')

class CategoryType(DjangoObjectType):
    class Meta: 
        model = Category
        fields = ('id','title')

class BookType(DjangoObjectType):
    class Meta: 
        model = Book
        fields = (
            'id',
            'title',
            'author',
            'isbn',
            'pages', 
            'price',
            'quantity', 
            'description',
            'status',
            'date_created',
        )  

class GroceryType(DjangoObjectType):
    class Meta:
        model = Grocery
        fields = (
            'product_tag',
            'name',
            'category',
            'price',
            'quantity',
            'imageurl',
            'status',
            'date_created',
        )

class Query(graphene.ObjectType):
    locations = graphene.List(LocationType)
    units = graphene.List(UnitsType)
    categories = graphene.List(CategoryType)
    books = graphene.List(BookType)
    groceries = graphene.List(GroceryType)

    def resolve_locations(root, info, **kwargs):
            # Querying a list
            return Location.objects.all()

    def resolve_units(root, info, **kwargs):
            # Querying a list
            return Units.objects.all()

    def resolve_books(root, info, **kwargs):
        # Querying a list
        return Book.objects.all()

    def resolve_categories(root, info, **kwargs):
        # Querying a list
        return Category.objects.all()

    def resolve_groceries(root, info, **kwargs):
        # Querying a list
        return Grocery.objects.all()
        
schema = graphene.Schema(query=Query)