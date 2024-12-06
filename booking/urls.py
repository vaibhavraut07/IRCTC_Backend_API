from django.urls import path
from . import views

app_name = 'booking'  # Add namespace

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('admin/add_train/', views.add_train, name='add_train'),
    path('seat-availability/', views.get_seat_availability, name='seat_availability'),
    path('book-seat/', views.book_seat, name='book_seat'),
    path('booking-details/', views.get_booking_details, name='booking_details'),
]