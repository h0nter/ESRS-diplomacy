from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from . import views


urlpatterns =[
    path('', views.index, name='index'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(template_name='host/login.html'), name='login'),
    # path('create_room/', views.create_room, name='create_room'),
    path('join_room/', views.join_room, name='join_room'),
    path('check_player/', views.check_player, name='check_player'),
    path('start_game/', views.start_game, name='start_game'),
    path('check_room_status/', views.check_room_status, name='check_room_status'),
    path('get_user_room_pk/', views.get_user_room_pk, name='get_user_room_names'),
]