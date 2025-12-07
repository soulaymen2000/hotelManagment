from django.urls import path
from .api_views import dashboard_stats, room_status_chart, booking_trend_chart, recent_activity

urlpatterns = [
    path('stats/', dashboard_stats, name='dashboard-stats'),
    path('charts/room-status/', room_status_chart, name='room-status-chart'),
    path('charts/booking-trend/', booking_trend_chart, name='booking-trend-chart'),
    path('recent-activity/', recent_activity, name='recent-activity'),
]