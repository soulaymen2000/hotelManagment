from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('management/', views.booking_management, name='booking-management'),
    path('create/', views.reception_booking_create, name='reception-booking-create'),
    path('guest/create/', views.guest_booking, name='guest-booking'),
    path('guest/list/', views.guest_booking_list, name='guest-booking-list'),
    path('<int:booking_id>/', views.booking_detail, name='booking-detail'),
]