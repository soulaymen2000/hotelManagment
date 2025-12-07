from django.test import TestCase
from django.contrib.auth import get_user_model
from bookings.models import Booking
from rooms.models import Room
from datetime import date, timedelta
from decimal import Decimal

User = get_user_model()


class BookingModelTest(TestCase):
    """Test cases for Booking model"""
    
    def setUp(self):
        """Set up test data"""
        self.guest = User.objects.create_user(
            email='guest@test.com',
            username='testguest',
            password='testpass123',
            role='guest'
        )
        
        self.room = Room.objects.create(
            number='101',
            room_type='Single',
            price_per_night=Decimal('100.00'),
            status='dispo',
            description='Test room'
        )
        
        self.check_in = date.today() + timedelta(days=1)
        self.check_out = date.today() + timedelta(days=3)
    
    def test_booking_creation(self):
        """Test creating a booking"""
        booking = Booking.objects.create(
            guest=self.guest,
            room=self.room,
            check_in_date=self.check_in,
            check_out_date=self.check_out,
            num_guests=2,
            total_price=Decimal('200.00'),
            status='pending'
        )
        
        self.assertEqual(booking.guest, self.guest)
        self.assertEqual(booking.room, self.room)
        self.assertEqual(booking.num_guests, 2)
        self.assertEqual(booking.status, 'pending')
    
    def test_booking_str_representation(self):
        """Test string representation of booking"""
        booking = Booking.objects.create(
            guest=self.guest,
            room=self.room,
            check_in_date=self.check_in,
            check_out_date=self.check_out,
            num_guests=1,
            total_price=Decimal('200.00')
        )
        
        expected_str = f"Booking {booking.id} - {self.room.number} - {self.guest.email}"
        self.assertEqual(str(booking), expected_str)
    
    def test_booking_price_calculation(self):
        """Test that total price is calculated correctly"""
        nights = (self.check_out - self.check_in).days
        expected_price = self.room.price_per_night * nights
        
        booking = Booking.objects.create(
            guest=self.guest,
            room=self.room,
            check_in_date=self.check_in,
            check_out_date=self.check_out,
            num_guests=1,
            total_price=expected_price
        )
        
        self.assertEqual(booking.total_price, expected_price)
    
    def test_booking_status_choices(self):
        """Test all status choices"""
        statuses = ['pending', 'confirmed', 'checked_in', 'checked_out', 'cancelled']
        
        for status_choice in statuses:
            booking = Booking.objects.create(
                guest=self.guest,
                room=self.room,
                check_in_date=self.check_in,
                check_out_date=self.check_out,
                num_guests=1,
                total_price=Decimal('200.00'),
                status=status_choice
            )
            self.assertEqual(booking.status, status_choice)
            booking.delete()  # Clean up
