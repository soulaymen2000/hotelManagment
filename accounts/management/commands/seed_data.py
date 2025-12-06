from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from rooms.models import Room

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **options):
        # Create admin user
        if not User.objects.filter(email='admin@hotel.com').exists():
            admin = User.objects.create_user(
                username='admin',
                email='admin@hotel.com',
                password='admin123',
                role='admin',
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created admin user: {admin.email}')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Admin user already exists')
            )

        # Create reception user
        if not User.objects.filter(email='reception@hotel.com').exists():
            reception = User.objects.create_user(
                username='reception',
                email='reception@hotel.com',
                password='reception123',
                role='reception',
                first_name='Reception',
                last_name='Staff'
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created reception user: {reception.email}')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Reception user already exists')
            )

        # Create sample rooms
        rooms_data = [
            {'number': '101', 'name': 'Single Room', 'floor': 1, 'capacity': 1, 'price_per_night': 100.00},
            {'number': '102', 'name': 'Double Room', 'floor': 1, 'capacity': 2, 'price_per_night': 150.00},
            {'number': '201', 'name': 'Deluxe Room', 'floor': 2, 'capacity': 2, 'price_per_night': 200.00},
            {'number': '202', 'name': 'Suite', 'floor': 2, 'capacity': 4, 'price_per_night': 300.00},
            {'number': '301', 'name': 'Presidential Suite', 'floor': 3, 'capacity': 6, 'price_per_night': 500.00},
        ]

        for room_data in rooms_data:
            room, created = Room.objects.get_or_create(
                number=room_data['number'],
                defaults={
                    'name': room_data['name'],
                    'floor': room_data['floor'],
                    'capacity': room_data['capacity'],
                    'price_per_night': room_data['price_per_night'],
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created room: {room.number}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Room {room.number} already exists')
                )

        self.stdout.write(
            self.style.SUCCESS('Database seeding completed!')
        )