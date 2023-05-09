import graphene
from .mutation.mutation import Mutation
from .query.query import Query
# from .query.broadcast import GameAPI


schema = graphene.Schema(query=Query, mutation=Mutation)