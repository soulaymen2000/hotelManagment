from django.db import models
from django.conf import settings


class AuditLog(models.Model):
    """
    Audit log model to track important actions in the system
    """
    ACTION_CHOICES = (
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('check_in', 'Check In'),
        ('check_out', 'Check Out'),
        ('room_status_change', 'Room Status Change'),
        ('booking_status_change', 'Booking Status Change'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=30, choices=ACTION_CHOICES)
    model_type = models.CharField(max_length=50)  # e.g., 'Room', 'Booking', 'User'
    object_id = models.PositiveIntegerField()
    description = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.action} on {self.model_type} by {self.user.username if self.user else 'System'}"
        
    class Meta:
        db_table = 'audit_logs'
        ordering = ['-created_at']