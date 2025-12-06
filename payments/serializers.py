from rest_framework import serializers
from .models import Payment
from bookings.models import Booking


class PaymentSerializer(serializers.ModelSerializer):
    booking_details = serializers.SerializerMethodField()
    
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('transaction_id',)
        
    def get_booking_details(self, obj):
        return {
            'id': obj.booking.id,
            'room_number': obj.booking.room.number,
            'guest_email': obj.booking.guest.email,
            'check_in_date': obj.booking.check_in_date,
            'check_out_date': obj.booking.check_out_date
        }


class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('booking', 'amount', 'payment_method')
        
    def validate(self, attrs):
        booking = attrs['booking']
        amount = attrs['amount']
        
        # Check if booking exists and is valid for payment
        if booking.status not in ['confirmed', 'checked_in']:
            raise serializers.ValidationError("Booking must be confirmed or checked in to process payment")
            
        # Check if amount matches booking total
        if amount != booking.total_price:
            raise serializers.ValidationError("Payment amount must match booking total price")
            
        return attrs
        
    def create(self, validated_data):
        # Generate a unique transaction ID
        import uuid
        validated_data['transaction_id'] = str(uuid.uuid4()).replace('-', '').upper()[:16]
        validated_data['status'] = 'completed'
        return super().create(validated_data)