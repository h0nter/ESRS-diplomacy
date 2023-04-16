
from django.contrib.auth.models import User
import graphene
from graphene import Mutation, String, InputObjectType
from .table_type import UserType

class UserInput(InputObjectType):
    username = String(required=True, description="Username for the new user")
    password = String(required=True, description="Password for the new user")


class CreateUserMutation(Mutation):
    class Arguments:
        input = UserInput(required=True, description="Input for creating a new user")
    
    user = graphene.Field(UserType)

    @staticmethod
    def mutate( root, info, input):
        # Create a new user
        print('adgafh')
        user = User.objects.create_user(username=input.username, password=input.password)
    
        return CreateUserMutation(user=user)
