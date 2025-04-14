# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('showtime/<int:showtime_id>/seats/', views.select_seats, name='select_seats'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('api/showtime/<int:showtime_id>/seats/', views.get_seat_data, name='get_seat_data'),
    path('api/book/', views.ajax_book_seats, name='ajax_book_seats'),

]
