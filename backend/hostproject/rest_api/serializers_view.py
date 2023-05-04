from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, MyTokenObtainPairSerializer, HostSerializer, PlayerRoomSerializer
from host.models import Host, PlayerRoom


class RegisterView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class HostCreateView(generics.ListCreateAPIView):
    queryset = Host.objects.all()
    serializer_class = HostSerializer


class HostUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Host.objects.all()
    serializer_class = HostSerializer


class PlayerRoomJoinView(generics.ListCreateAPIView):
    queryset = PlayerRoom.objects.all()
    serializer_class = PlayerRoomSerializer


class PlayerRoomUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlayerRoom.objects.all()
    serializer_class = PlayerRoomSerializer