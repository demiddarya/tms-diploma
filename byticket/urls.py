from django.urls import path

from . import views

app_name = 'byticket'
urlpatterns = [
    path('welcome', views.welcome, name='welcome'),
    path('auth', views.auth, name='auth'),
    path('register', views.register, name='register'),

]
