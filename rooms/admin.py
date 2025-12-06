from django.contrib import admin
from .models import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'floor', 'capacity', 'price_per_night', 'status', 'created_at')
    list_filter = ('status', 'floor', 'capacity')
    search_fields = ('number', 'name')
    list_editable = ('status',)
    ordering = ('number',)