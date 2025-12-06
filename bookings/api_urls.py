from django.urls import path
from .api_views import (
    GuestBookingCreateView, GuestBookingListView,
    ReceptionBookingListView, ReceptionBookingCreateView,
    ReceptionBookingStatusUpdateView, ReceptionBookingDetailView
)

urlpatterns = [
    path('guest/create/', GuestBookingCreateView.as_view(), name='guest-booking-create'),
    path('guest/list/', GuestBookingListView.as_view(), name='guest-booking-list'),
    path('reception/', ReceptionBookingListView.as_view(), name='reception-booking-list'),
    path('reception/create/', ReceptionBookingCreateView.as_view(), name='reception-booking-create'),
    path('reception/<int:pk>/', ReceptionBookingDetailView.as_view(), name='reception-booking-detail'),
    path('reception/<int:pk>/status/', ReceptionBookingStatusUpdateView.as_view(), name='reception-booking-status-update'),
]