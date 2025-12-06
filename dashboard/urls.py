from django.urls import path
from . import views

urlpatterns = [
    path('reception/', views.reception_dashboard, name='reception-dashboard'),
    path('guest/', views.guest_dashboard, name='guest-dashboard'),
    path('admin/', views.admin_dashboard, name='admin-dashboard'),
]