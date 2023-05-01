from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from . import views, register


urlpatterns =[
    path('', views.index, name='index'),
    path('register/', register.registration, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(template_name='host/login.html'), name='login'),
    path('launch_room/', views.launch_room, name='launch_room'),
    path('get_csrf', views.get_csrf, name='get_csrf'),
    path('get_login', views.login_view, name='get_login')
]