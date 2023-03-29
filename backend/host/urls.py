from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView
from . import views



urlpatterns =[
    path('', views.index, name='index'),
    path('register/', views.registration, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(template_name='host/login.html'), name='login'),
]