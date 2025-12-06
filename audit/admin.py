from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'model_type', 'user', 'object_id', 'created_at')
    list_filter = ('action', 'model_type', 'created_at')
    search_fields = ('user__username', 'description')
    readonly_fields = ('user', 'action', 'model_type', 'object_id', 'description', 'ip_address', 'created_at')
    ordering = ('-created_at',)