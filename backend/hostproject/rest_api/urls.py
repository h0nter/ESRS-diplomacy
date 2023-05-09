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
    path('player_list/', views.player_list, name='player_list'),
    path('host_status/', views.host_status, name='host_status'),
]

