from django.urls import path

from . import views

app_name = 'byticket'
urlpatterns = [
    path('movies/movie/<int:movie_id>', views.movie_detail_request, name='movie_detail'),
    path('movies/category/<int:category_id>', views.movies_by_category_request, name='movies_by_category'),
    path('cinemas/cinema/<int:cinema_id>', views.cinema_detail_request, name='cinema_detail'),
    path('screenings/screening/<int:screening_id>', views.screening_detail_request, name='screening_detail'),
    path('screenings/screening/reserve_seats', views.reserve_seats_request, name='reserve_seats'),
    path('welcome/', views.welcome_request, name='welcome'),
    path('login/', views.login_request, name='login'),
    path('register/', views.register_request, name='register'),
    path('logout/', views.logout_request, name='logout'),
    path('movies/', views.movies_list_request, name='movies'),
    path('cinemas/', views.cinemas_list_request, name='cinemas'),
    path('profile/', views.profile_request, name='profile'),
    path('profile/ticket/pdf/<int:ticket_id>', views.ticket_pdf_request, name='ticket_pdf'),
    path('profile/ticket/delete/<int:ticket_id>', views.ticket_delete_request, name='ticket_delete'),
    path('reservation/success', views.reservation_success_request, name='reservation_success'),
    path('reservation/failed', views.reservation_failed_request, name='reservation_failed'),
    path('api/purchased_tickets/<int:screening_id>', views.get_purchased_tickets, name='get_purchased_tickets'),
    path('', views.welcome_request, name='startup'),
]