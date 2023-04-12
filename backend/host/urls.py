from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from . import views, register


urlpatterns =[
    path('register/', register.registration, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(template_name='host/login.html'), name='login'),
    path('launch_room/', views.launch_room, name='launch_room'),
    path('invitations/', views.invitations, name='invitation'),
]
