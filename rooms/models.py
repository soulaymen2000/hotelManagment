from django.db import models
from django.conf import settings


class Room(models.Model):
    """
    Room model with status tracking
    """
    STATUS_CHOICES = (
        ('dispo', 'Available'),
        ('reserved', 'Reserved'),
        ('booked', 'Booked'),
        ('maintenance', 'Maintenance'),
    )
    
    number = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    floor = models.IntegerField()
    capacity = models.IntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='dispo')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Room {self.number} - {self.name} ({self.status})"
        
    class Meta:
        db_table = 'rooms'
        ordering = ['number']