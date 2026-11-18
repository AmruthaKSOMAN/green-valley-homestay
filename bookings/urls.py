
from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('book/', views.create_booking, name='create_booking'),
    path('booking-success/', views.booking_success, name='booking_success'),

    path(
        'confirm/<int:booking_id>/',
        views.confirm_booking,
        name='confirm_booking'
    ),

    path(
        'cancel/<int:booking_id>/',
        views.cancel_booking,
        name='cancel_booking'
    ),
]
