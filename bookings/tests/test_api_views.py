from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from bookings.models import Booking
from rooms.models import Room
from datetime import date, timedelta
from decimal import Decimal

User = get_user_model()


class BookingAPITest(APITestCase):
    """Test cases for Booking API views"""
    
    def setUp(self):
        """Set up test data"""
        # Create users
        self.guest = User.objects.create_user(
            email='guest@test.com',
            username='guest',
            password='testpass123',
            role='guest'
        )
        
        self.reception = User.objects.create_user(
            email='reception@test.com',
            username='reception',
            password='testpass123',
            role='reception'
        )
        
        # Create room
        self.room = Room.objects.create(
            number='101',
            room_type='Single',
            price_per_night=Decimal('100.00'),
            status='dispo',
            description='Test room'
        )
        
        self.check_in = str(date.today() + timedelta(days=1))
        self.check_out = str(date.today() + timedelta(days=3))
        
        self.client = APIClient()
    
    def test_guest_booking_creation_sets_room_to_reserved(self):
        """Test that guest booking sets room status to 'reserved'"""
        self.client.force_authenticate(user=self.guest)
        
        booking_data = {
            'room': self.room.id,
            'check_in_date': self.check_in,
            'check_out_date': self.check_out,
            'num_guests': 2
        }
        
        response = self.client.post('/api/bookings/guest/create/', booking_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check room status changed to reserved
        self.room.refresh_from_db()
        self.assertEqual(self.room.status, 'reserved')
        
        # Check booking status is pending
        booking = Booking.objects.get(id=response.data['id'])
        self.assertEqual(booking.status, 'pending')
    
    def test_reception_booking_creation_sets_room_to_booked(self):
        """Test that reception booking sets room status to 'booked' and booking to 'confirmed'"""
        self.client.force_authenticate(user=self.reception)
        
        booking_data = {
            'guest_email': self.guest.email,
            'room': self.room.id,
            'check_in_date': self.check_in,
            'check_out_date': self.check_out,
            'num_guests': 2
        }
        
        response = self.client.post('/api/bookings/reception/create/', booking_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check room status changed to booked
        self.room.refresh_from_db()
        self.assertEqual(self.room.status, 'booked')
        
        # Check booking status is confirmed
        booking = Booking.objects.get(id=response.data['id'])
        self.assertEqual(booking.status, 'confirmed')
    
    def test_guest_cannot_create_booking_without_auth(self):
        """Test that unauthenticated users cannot create bookings"""
        booking_data = {
            'room': self.room.id,
            'check_in_date': self.check_in,
            'check_out_date': self.check_out,
            'num_guests': 2
        }
        
        response = self.client.post('/api/bookings/guest/create/', booking_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_guest_can_list_own_bookings(self):
        """Test that guests can list their own bookings"""
        # Create a booking for the guest
        Booking.objects.create(
            guest=self.guest,
            room=self.room,
            check_in_date=self.check_in,
            check_out_date=self.check_out,
            num_guests=1,
            total_price=Decimal('200.00'),
            status='pending'
        )
        
        self.client.force_authenticate(user=self.guest)
        response = self.client.get('/api/bookings/guest/list/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)
    
    def test_reception_can_list_all_bookings(self):
        """Test that reception can list all bookings"""
        # Create bookings for different guests
        Booking.objects.create(
            guest=self.guest,
            room=self.room,
            check_in_date=self.check_in,
            check_out_date=self.check_out,
            num_guests=1,
            total_price=Decimal('200.00'),
            status='pending'
        )
        
        self.client.force_authenticate(user=self.reception)
        response = self.client.get('/api/bookings/reception/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
