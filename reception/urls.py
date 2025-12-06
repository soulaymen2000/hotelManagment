from django.urls import path
from .views import (
    check_in_guest, check_out_guest, 
    mark_room_maintenance, finish_room_maintenance
)

urlpatterns = [
    path('check-in/<int:booking_id>/', check_in_guest, name='check-in-guest'),
    path('check-out/<int:booking_id>/', check_out_guest, name='check-out-guest'),
    path('room/<int:room_id>/maintenance/start/', mark_room_maintenance, name='mark-room-maintenance'),
    path('room/<int:room_id>/maintenance/finish/', finish_room_maintenance, name='finish-room-maintenance'),
]