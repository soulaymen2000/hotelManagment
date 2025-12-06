from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'guest', 'room', 'check_in_date', 'check_out_date', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'check_in_date', 'check_out_date')
    search_fields = ('guest__username', 'guest__email', 'room__number')
    ordering = ('-created_at',)