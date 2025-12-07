from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


@login_required
def booking_management(request):
    """Booking management view for reception staff"""
    if not request.user.is_reception():
        return redirect('home')
    return render(request, 'bookings/booking_management.html')


@login_required
def guest_booking(request):
    """Guest booking view"""
    if not request.user.is_guest():
        return redirect('home')
    return render(request, 'bookings/guest_booking.html')


@login_required
def booking_detail(request, booking_id):
    """Booking detail view"""
    # In a real application, you would fetch the booking from the database
    # For now, we'll just render the template
    return render(request, 'bookings/booking_detail.html')


@login_required
def reception_booking_create(request):
    """Reception booking creation view"""
    if not request.user.is_reception() and not request.user.is_admin():
        return redirect('home')
    return render(request, 'bookings/reception_booking_create.html')