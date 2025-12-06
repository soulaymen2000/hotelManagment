from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rooms.models import Room
from bookings.models import Booking
from payments.models import Payment
from accounts.models import User
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import datetime, timedelta


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    user = request.user
    
    # Different stats based on user role
    if user.is_admin():
        return admin_dashboard_stats()
    elif user.is_reception():
        return reception_dashboard_stats()
    else:  # guest
        return guest_dashboard_stats()


def admin_dashboard_stats():
    """Admin dashboard statistics"""
    # Get today's date
    today = timezone.now().date()
    
    # Room statistics
    total_rooms = Room.objects.count()
    available_rooms = Room.objects.filter(status='dispo').count()
    reserved_rooms = Room.objects.filter(status='reserved').count()
    booked_rooms = Room.objects.filter(status='booked').count()
    maintenance_rooms = Room.objects.filter(status='maintenance').count()
    
    # Booking statistics
    total_bookings = Booking.objects.count()
    pending_bookings = Booking.objects.filter(status='pending').count()
    confirmed_bookings = Booking.objects.filter(status='confirmed').count()
    checked_in_bookings = Booking.objects.filter(status='checked_in').count()
    checked_out_bookings = Booking.objects.filter(status='checked_out').count()
    cancelled_bookings = Booking.objects.filter(status='cancelled').count()
    
    # User statistics
    total_users = User.objects.count()
    guests = User.objects.filter(role='guest').count()
    receptionists = User.objects.filter(role='reception').count()
    admins = User.objects.filter(role='admin').count()
    
    # Revenue statistics
    total_revenue = Payment.objects.filter(
        status='completed'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    data = {
        'rooms': {
            'total': total_rooms,
            'available': available_rooms,
            'reserved': reserved_rooms,
            'booked': booked_rooms,
            'maintenance': maintenance_rooms
        },
        'bookings': {
            'total': total_bookings,
            'pending': pending_bookings,
            'confirmed': confirmed_bookings,
            'checked_in': checked_in_bookings,
            'checked_out': checked_out_bookings,
            'cancelled': cancelled_bookings
        },
        'payments': {
            'total_revenue': float(total_revenue)
        },
        'users': {
            'total': total_users,
            'guests': guests,
            'receptionists': receptionists,
            'admins': admins
        }
    }
    
    return Response(data)


def reception_dashboard_stats():
    """Reception dashboard statistics"""
    # Get today's date
    today = timezone.now().date()
    
    # Room statistics
    total_rooms = Room.objects.count()
    available_rooms = Room.objects.filter(status='dispo').count()
    reserved_rooms = Room.objects.filter(status='reserved').count()
    booked_rooms = Room.objects.filter(status='booked').count()
    maintenance_rooms = Room.objects.filter(status='maintenance').count()
    
    # Booking statistics
    total_bookings = Booking.objects.count()
    pending_bookings = Booking.objects.filter(status='pending').count()
    confirmed_bookings = Booking.objects.filter(status='confirmed').count()
    checked_in_bookings = Booking.objects.filter(status='checked_in').count()
    checked_out_bookings = Booking.objects.filter(status='checked_out').count()
    cancelled_bookings = Booking.objects.filter(status='cancelled').count()
    
    # Today's check-ins and check-outs
    todays_check_ins = Booking.objects.filter(
        check_in_date=today,
        status='confirmed'
    ).count()
    
    todays_check_outs = Booking.objects.filter(
        check_out_date=today,
        status='checked_in'
    ).count()
    
    # Recent bookings (last 7 days)
    week_ago = today - timedelta(days=7)
    recent_bookings = Booking.objects.filter(
        created_at__date__gte=week_ago
    ).count()
    
    # Revenue statistics
    total_revenue = Payment.objects.filter(
        status='completed'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Recent payments (last 7 days)
    recent_payments = Payment.objects.filter(
        paid_at__date__gte=week_ago,
        status='completed'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    data = {
        'rooms': {
            'total': total_rooms,
            'available': available_rooms,
            'reserved': reserved_rooms,
            'booked': booked_rooms,
            'maintenance': maintenance_rooms
        },
        'bookings': {
            'total': total_bookings,
            'pending': pending_bookings,
            'confirmed': confirmed_bookings,
            'checked_in': checked_in_bookings,
            'checked_out': checked_out_bookings,
            'cancelled': cancelled_bookings,
            'todays_check_ins': todays_check_ins,
            'todays_check_outs': todays_check_outs,
            'recent': recent_bookings
        },
        'payments': {
            'total_revenue': float(total_revenue),
            'recent_revenue': float(recent_payments)
        }
    }
    
    return Response(data)


def guest_dashboard_stats():
    """Guest dashboard statistics"""
    # For guests, we only show their own bookings
    user = User.objects.get(id=request.user.id)
    user_bookings = Booking.objects.filter(guest=user)
    
    total_bookings = user_bookings.count()
    pending_bookings = user_bookings.filter(status='pending').count()
    confirmed_bookings = user_bookings.filter(status='confirmed').count()
    checked_in_bookings = user_bookings.filter(status='checked_in').count()
    checked_out_bookings = user_bookings.filter(status='checked_out').count()
    cancelled_bookings = user_bookings.filter(status='cancelled').count()
    
    # Calculate total spent by guest
    total_spent = Payment.objects.filter(
        booking__guest=user,
        status='completed'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    data = {
        'bookings': {
            'total': total_bookings,
            'pending': pending_bookings,
            'confirmed': confirmed_bookings,
            'checked_in': checked_in_bookings,
            'checked_out': checked_out_bookings,
            'cancelled': cancelled_bookings
        },
        'payments': {
            'total_spent': float(total_spent)
        }
    }
    
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def room_status_chart(request):
    user = request.user
    
    # Different chart data based on user role
    if user.is_admin() or user.is_reception():
        # Admin and reception can see room status chart
        # Get room status distribution
        status_data = Room.objects.values('status').annotate(count=Count('status'))
        
        # Convert to chart-friendly format
        chart_data = []
        status_labels = {
            'dispo': 'Available',
            'reserved': 'Reserved',
            'booked': 'Booked',
            'maintenance': 'Maintenance'
        }
        
        for item in status_data:
            chart_data.append({
                'status': status_labels.get(item['status'], item['status']),
                'count': item['count']
            })
        
        return Response(chart_data)
    else:
        # Guests don't have access to room status chart
        return Response({
            'error': 'Access denied'
        }, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def booking_trend_chart(request):
    user = request.user
    
    # Different chart data based on user role
    if user.is_admin() or user.is_reception():
        # Admin and reception can see booking trend chart
        # Get bookings for the last 30 days
        thirty_days_ago = timezone.now() - timedelta(days=30)
        bookings = Booking.objects.filter(
            created_at__gte=thirty_days_ago
        ).extra(select={'date': 'date(created_at)'}).values('date').annotate(count=Count('id')).order_by('date')
        
        # Convert to chart-friendly format
        chart_data = []
        for booking in bookings:
            chart_data.append({
                'date': booking['date'],
                'count': booking['count']
            })
        
        return Response(chart_data)
    elif user.is_guest():
        # Guests can see their own booking trend
        thirty_days_ago = timezone.now() - timedelta(days=30)
        bookings = Booking.objects.filter(
            guest=user,
            created_at__gte=thirty_days_ago
        ).extra(select={'date': 'date(created_at)'}).values('date').annotate(count=Count('id')).order_by('date')
        
        # Convert to chart-friendly format
        chart_data = []
        for booking in bookings:
            chart_data.append({
                'date': booking['date'],
                'count': booking['count']
            })
        
        return Response(chart_data)
    else:
        # Unauthorized access
        return Response({
            'error': 'Access denied'
        }, status=status.HTTP_403_FORBIDDEN)