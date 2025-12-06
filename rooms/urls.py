from django.urls import path
from . import views

urlpatterns = [
    path('management/', views.room_management, name='room-management'),
    path('<int:room_id>/', views.room_detail, name='room-detail'),
]