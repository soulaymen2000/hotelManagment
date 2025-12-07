"""
Script to create sample data for testing hotel management system
Run with: python manage.py shell < create_sample_data.py
"""
from django.utils import timezone
from datetime import timedelta
from rooms.models import Room
from bookings.models import Booking
from payments.models import Payment
from accounts.models import User

# Get or create test user
guest_user, created = User.objects.get_or_create(
    email='guest@example.com',
    defaults={
        'first_name': 'Test',
        'last_name': 'Guest',
        'role': 'guest',
        'phone_number': '+1234567890'
    }
)
if created:
    guest_user.set_password('password123')
    guest_user.save()
    print(f"Created guest user: {guest_user.email}")
else:
    print(f"Using existing guest user: {guest_user.email}")

# Get available rooms
rooms = Room.objects.all()[:3]  # Get first 3 rooms
print(f"Found {rooms.count()} rooms")

# Create sample bookings
today = timezone.now().date()
bookings_created = 0

for i, room in enumerate(rooms):
    # Create a booking
    check_in = today + timedelta(days=i)
    check_out = check_in + timedelta(days=3)
    
    booking = Booking.objects.create(
        guest=guest_user,
        room=room,
        check_in_date=check_in,
        check_out_date=check_out,
        status='confirmed' if i == 0 else 'pending',
        number_of_guests=2,
        special_requests='Test booking' if i < 2 else ''
    )
    bookings_created += 1
    print(f"Created booking {booking.id}: Room {room.number}, {check_in} to {check_out}")
    
    # Create payment for confirmed booking
    if booking.status == 'confirmed':
        total_nights = (check_out - check_in).days
        amount = room.price_per_night * total_nights
        
        payment = Payment.objects.create(
            booking=booking,
            amount=amount,
            payment_method='credit_card',
            status='completed'
        )
        print(f"Created payment {payment.id}: ${amount}")

print(f"\nSummary:")
print(f"- Rooms: {Room.objects.count()}")
print(f"- Bookings: {Booking.objects.count()}")
print(f"- Payments: {Payment.objects.count()}")
