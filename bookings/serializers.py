from rest_framework import serializers
from .models import Booking
from rooms.models import Room
from accounts.models import User


class BookingSerializer(serializers.ModelSerializer):
    guest_email = serializers.EmailField(source='guest.email', read_only=True)
    room_number = serializers.CharField(source='room.number', read_only=True)
    
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ('guest', 'total_price')
        
        
class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('room', 'check_in_date', 'check_out_date', 'num_guests')
        
    def validate(self, attrs):
        # Check if room is available for the given dates
        room = attrs['room']
        check_in = attrs['check_in_date']
        check_out = attrs['check_out_date']
        
        if check_in >= check_out:
            raise serializers.ValidationError("Check-out date must be after check-in date")
            
        # Check for overlapping bookings
        overlapping_bookings = Booking.objects.filter(
            room=room,
            status__in=['confirmed', 'checked_in'],
            check_in_date__lt=check_out,
            check_out_date__gt=check_in
        )
        
        if overlapping_bookings.exists():
            raise serializers.ValidationError("Room is not available for the selected dates")
            
        return attrs
        
    def create(self, validated_data):
        # Calculate total price based on room price and number of nights
        room = validated_data['room']
        check_in = validated_data['check_in_date']
        check_out = validated_data['check_out_date']
        
        nights = (check_out - check_in).days
        validated_data['total_price'] = room.price_per_night * nights
        validated_data['status'] = 'pending'
        
        return super().create(validated_data)


class BookingStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('status',)