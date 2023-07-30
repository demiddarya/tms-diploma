from django.urls import path

from . import views

app_name = 'byticket'
urlpatterns = [
    path('welcome', views.welcome_request, name='welcome'),
    path('login', views.login_request, name='login'),
    path('register', views.register_request, name='register'),
    path('logout', views.logout_request, name="logout"),
    path('home', views.home_request, name="home")
]