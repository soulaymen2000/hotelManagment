from django.urls import path
from . import views

urlpatterns = [
    path('management/', views.booking_management, name='booking-management'),
    path('guest/create/', views.guest_booking, name='guest-booking'),
    path('<int:booking_id>/', views.booking_detail, name='booking-detail'),
]