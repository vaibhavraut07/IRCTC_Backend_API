from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),

    # Admin endpoints - Remove extra 'api/' prefix
    path('admin/add_train/', views.add_train, name='add_train'),
    
    # User endpoints - Remove extra 'api/' prefix
    path('get_seat_availability/', views.get_seat_availability, name='get_seat_availability'),
    path('book_seat/', views.book_seat, name='book_seat'),
    path('get_booking_details/', views.get_booking_details, name='get_booking_details'),
]