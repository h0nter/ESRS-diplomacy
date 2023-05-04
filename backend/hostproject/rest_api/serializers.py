from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from host.models import Host, PlayerRoom


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'username': {'required': True},
            'password': {'required': True}
        }

    def create(self, user_data):
        user = User.objects.create(
            username=user_data['username'],
            email=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name']
        )
        
        user.set_password(user_data['password'])
        user.save()

        return user
    

class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = '__all__'


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        # Add custom claims
        token['username'] = user.username
        return token


class PlayerRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerRoom
        fields = '__all__'