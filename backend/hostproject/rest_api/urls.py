from django.urls import path
from . import serializers_view, views

urlpatterns =[
    path('', views.hello_world, name='hello_word'),
    path('register/', serializers_view.RegisterView.as_view(), name='register'),
    path('login/', serializers_view.MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('host/', serializers_view.HostCreateView.as_view(), name='host_RC'),
    path('host/<pk>/', serializers_view.HostUpdateDestroyView.as_view(), name='host_UD'),
    path('player/', serializers_view.PlayerRoomJoinView.as_view(), name='player_RC'),
    path('player/<pk>/', serializers_view.PlayerRoomUpdateDestroyView.as_view(), name='player_UD'),
    # simple api
    path('get_login/', views.get_login, name='get_login'),
    path('start_game/', views.start_game, name='start_game'),
    # path('create_room/', views.create_room, name='create_room'),
    # path('join_room/', views.join_room, name='join_room'),
    # path('check_player/', views.check_player, name='check_player'),
    # path('check_room_status/', views.check_room_status, name='check_room_status'),
    # path('get_user_room_pk/', views.get_user_room_pk, name='get_user_room_names'),
]

