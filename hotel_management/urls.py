"""hotel_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False), name='home'),
    path('test-layout/', views.test_layout, name='test-layout'),
    path('logout/', views.logout_view, name='logout'),
    path('accounts/', include('accounts.urls')),
    path('dashboards/', include('dashboard.urls')),
    path('bookings/', include('bookings.urls', namespace='bookings')),
    path('rooms/', include('rooms.urls', namespace='rooms')),
    path('audit/', include('audit.urls')),
    # API endpoints
    path('api/dashboard/', include('dashboard.api_urls')),
    path('api/bookings/', include('bookings.api_urls')),
    path('api/rooms/', include('rooms.api_urls')),
    path('api/payments/', include('payments.urls')),
    path('api/accounts/', include('accounts.api_urls')),
]