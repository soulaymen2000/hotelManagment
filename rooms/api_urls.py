from django.urls import path
from .api_views import (
    RoomListView, RoomDetailView, ReceptionRoomListView, 
    ReceptionRoomStatusUpdateView, AdminRoomListView
)

urlpatterns = [
    path('', RoomListView.as_view(), name='room-list'),
    path('<int:pk>/', RoomDetailView.as_view(), name='room-detail'),
    path('reception/', ReceptionRoomListView.as_view(), name='reception-room-list'),
    path('reception/<int:pk>/status/', ReceptionRoomStatusUpdateView.as_view(), name='reception-room-status-update'),
    path('admin/', AdminRoomListView.as_view(), name='admin-room-list'),
]