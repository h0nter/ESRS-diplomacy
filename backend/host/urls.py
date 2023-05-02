from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from . import views, register


urlpatterns =[
    path('', views.index, name='index'),
    path('register/', register.registration, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(template_name='host/login.html'), name='login'),
    path('launch_room/', views.launch_room, name='launch_room'),
    path('get_login/', views.get_login, name='get_login'),
    path('create_room/', views.create_room, name='create_room'),
    path('join_room/', views.join_room, name='join_room'),
    path('check_player/', views.check_player, name='check_player'),
    path('start_game/', views.start_game, name='start_game'),
    path('check_room_status/', views.check_room_status, name='check_room_status'),
]