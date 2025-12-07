from django.urls import path
from django.urls import path
from . import views

app_name = 'rooms'

urlpatterns = [
    path('management/', views.room_management, name='room-management'),
    path('create/', views.room_create, name='room-create'),
    path('<int:room_id>/', views.room_detail, name='room-detail'),
]