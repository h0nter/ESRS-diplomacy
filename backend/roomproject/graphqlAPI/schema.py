import graphene
from .mutation.mutation import Mutation
from .query.query import Query


schema = graphene.Schema(query=Query, mutation=Mutation)