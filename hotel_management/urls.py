"""
URL configuration for hotel_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . import views

schema_view = get_schema_view(
   openapi.Info(
      title="Hotel Management API",
      default_version='v1',
      description="API for hotel management system",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@hotel.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard_redirect, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('rooms/', include('rooms.urls')),
    path('bookings/', include('bookings.urls')),
    path('dashboards/', include('dashboard.urls')),  # Changed from 'dashboard/' to 'dashboards/' to avoid conflict
    path('api/auth/', include('accounts.api_urls')),
    path('api/rooms/', include('rooms.api_urls')),
    path('api/bookings/', include('bookings.api_urls')),
    path('api/payments/', include('payments.urls')),
    path('api/dashboard/', include('dashboard.api_urls')),
    path('api/reception/', include('reception.urls')),
    path('api/audit/', include('audit.urls')),
    # Swagger documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]