# Hotel Management System

A complete hotel management system built with Django 5.2.8 and Django REST Framework.

## Features

### User Roles & Permissions
- **Admin**: Can only change user roles and delete users (cannot delete or modify another Admin, cannot modify bookings or manage rooms)
- **Reception**: Has access to dashboard, reception booking interface, room management, confirm bookings (check-in), and process check-out
- **Guest**: Can create a booking through public form

### Room Status Logic
- `dispo` → Available
- `reserved` → Reserved by a normal user
- `booked` → When receptionist confirms check-in
- `maintenance` → Taken for maintenance

### Room Lifecycle Rules
1. Normal User Creates Reservation → Room auto becomes reserved
2. Reception Confirms Arrival (Check-in) → Reserved → Booked
3. Checkout by Reception → Booked → Dispo
4. Maintenance → Reception can mark any dispo room as maintenance → Maintenance → Dispo when finished

### Booking Logic
- Reception can create, modify, cancel any booking, confirm check-in, and process check-out
- Guest can create booking via public form (creates status reserved) but has no access to modify anything

### Authentication & Security
- Email login system
- JWT authentication (SimpleJWT)
- Strict role-based permission system
- Admin cannot delete or downgrade another admin

## System Architecture

- Django 5.2.8
- Django REST Framework
- Tailwind CSS templates
- SQLite for development
- Modules: accounts, rooms, bookings, payments, dashboard, reception, audit

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/token/` - Obtain JWT token
- `POST /api/auth/token/refresh/` - Refresh JWT token

### User Management (Admin only)
- `GET /api/auth/admin/users/` - List all users
- `GET/PUT/DELETE /api/auth/admin/users/{id}/` - User detail/update/delete

### Rooms
- `GET /api/rooms/` - List all rooms
- `GET /api/rooms/{id}/` - Room detail
- `GET/POST /api/rooms/reception/` - Reception room management
- `PUT /api/rooms/reception/{id}/status/` - Update room status

### Bookings
- `POST /api/bookings/guest/create/` - Guest creates booking
- `GET /api/bookings/guest/list/` - Guest booking list
- `GET/POST /api/bookings/reception/` - Reception booking management
- `GET/PUT/DELETE /api/bookings/reception/{id}/` - Booking detail/update/delete
- `PUT /api/bookings/reception/{id}/status/` - Update booking status

### Payments
- `GET /api/payments/` - List payments
- `POST /api/payments/create/` - Create payment
- `GET /api/payments/reception/` - Reception payment list

### Dashboard
- `GET /api/dashboard/stats/` - Dashboard statistics
- `GET /api/dashboard/charts/room-status/` - Room status chart data
- `GET /api/dashboard/charts/booking-trend/` - Booking trend chart data

### Reception Workflows
- `POST /api/reception/check-in/{booking_id}/` - Check-in guest
- `POST /api/reception/check-out/{booking_id}/` - Check-out guest
- `POST /api/reception/room/{room_id}/maintenance/start/` - Mark room for maintenance
- `POST /api/reception/room/{room_id}/maintenance/finish/` - Finish room maintenance

### Audit Logs
- `GET /api/audit/` - List audit logs

## Frontend Templates

### Dashboard Templates
- **Reception Dashboard** (`templates/dashboard/reception_dashboard.html`): Interactive charts and statistics for reception staff
- **Guest Dashboard** (`templates/dashboard/guest_dashboard.html`): Booking overview and management for guests
- **Admin Dashboard** (`templates/dashboard/admin_dashboard.html`): System-wide statistics and user management

### Authentication Templates
- **Login Page** (`templates/registration/login.html`): Secure login form with role-based redirection
- **Registration Page** (`templates/registration/register.html`): User registration form
- **Profile Page** (`templates/registration/profile.html`): User profile management

### Room Management Templates
- **Room Management** (`templates/rooms/room_management.html`): Filterable room listings and status management
- **Room Detail** (`templates/rooms/room_detail.html`): Detailed view of a specific room

### Booking Management Templates
- **Booking Management** (`templates/bookings/booking_management.html`): Comprehensive booking listing and management
- **Guest Booking** (`templates/bookings/guest_booking.html`): Intuitive booking form for guests
- **Booking Detail** (`templates/bookings/booking_detail.html`): Detailed view of a specific booking

### Payment Templates
- **Payment Form** (`templates/payments/payment_form.html`): Secure payment processing form
- **Payment Detail** (`templates/payments/payment_detail.html`): Detailed view of a payment transaction

### Audit Templates
- **Audit Log** (`templates/audit/audit_log.html`): System activity tracking and filtering

## Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```
   python manage.py migrate
   ```
4. Seed initial data:
   ```
   python manage.py seed_data
   ```
5. Run the development server:
   ```
   python manage.py runserver
   ```

## Testing the API

Use the provided test scripts or tools like Postman to test the API endpoints.

## Swagger Documentation

Visit `http://127.0.0.1:8000/swagger/` for interactive API documentation.

## Seeded Data

The system comes with pre-seeded data:
- Admin user: admin@hotel.com / admin123
- Reception user: reception@hotel.com / reception123
- 5 sample rooms (101, 102, 201, 202, 301)