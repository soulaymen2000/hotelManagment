from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rooms.models import Room
from bookings.models import Booking
from payments.models import Payment
from accounts.models import User
from rooms.serializers import RoomStatusUpdateSerializer
from bookings.serializers import BookingStatusUpdateSerializer
from audit.models import AuditLog


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_in_guest(request, booking_id):
    """
    Check-in a guest by changing booking status to 'checked_in'
    and room status to 'booked'
    """
    user = request.user
    
    # Only reception staff can check-in guests
    if not user.is_reception():
        return Response({
            'error': 'Only reception staff can check-in guests'
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        booking = Booking.objects.get(id=booking_id)
    except Booking.DoesNotExist:
        return Response({
            'error': 'Booking not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Check if booking is in correct status for check-in
    if booking.status != 'confirmed':
        return Response({
            'error': 'Booking must be confirmed to check-in'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Update booking status
    old_status = booking.status
    booking.status = 'checked_in'
    booking.save()
    
    # Update room status
    room = booking.room
    room.status = 'booked'
    room.save()
    
    # Log the actions
    AuditLog.objects.create(
        user=user,
        action='booking_status_change',
        model_type='Booking',
        object_id=booking.id,
        description=f'Changed booking status from {old_status} to checked_in (check-in)'
    )
    
    AuditLog.objects.create(
        user=user,
        action='room_status_change',
        model_type='Room',
        object_id=room.id,
        description=f'Changed room {room.number} status to booked (check-in)'
    )
    
    return Response({
        'message': 'Guest checked-in successfully',
        'booking_id': booking.id,
        'room_number': room.number
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_out_guest(request, booking_id):
    """
    Check-out a guest by changing booking status to 'checked_out'
    and room status to 'dispo'
    """
    user = request.user
    
    # Only reception staff can check-out guests
    if not user.is_reception():
        return Response({
            'error': 'Only reception staff can check-out guests'
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        booking = Booking.objects.get(id=booking_id)
    except Booking.DoesNotExist:
        return Response({
            'error': 'Booking not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Check if booking is in correct status for check-out
    if booking.status != 'checked_in':
        return Response({
            'error': 'Booking must be checked-in to check-out'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Update booking status
    old_status = booking.status
    booking.status = 'checked_out'
    booking.save()
    
    # Update room status
    room = booking.room
    room.status = 'dispo'
    room.save()
    
    # Log the actions
    AuditLog.objects.create(
        user=user,
        action='booking_status_change',
        model_type='Booking',
        object_id=booking.id,
        description=f'Changed booking status from {old_status} to checked_out (check-out)'
    )
    
    AuditLog.objects.create(
        user=user,
        action='room_status_change',
        model_type='Room',
        object_id=room.id,
        description=f'Changed room {room.number} status to available (check-out)'
    )
    
    return Response({
        'message': 'Guest checked-out successfully',
        'booking_id': booking.id,
        'room_number': room.number
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_room_maintenance(request, room_id):
    """
    Mark a room as under maintenance
    """
    user = request.user
    
    # Only reception staff can mark rooms for maintenance
    if not user.is_reception():
        return Response({
            'error': 'Only reception staff can mark rooms for maintenance'
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        room = Room.objects.get(id=room_id)
    except Room.DoesNotExist:
        return Response({
            'error': 'Room not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Update room status
    old_status = room.status
    room.status = 'maintenance'
    room.save()
    
    # Log the action
    AuditLog.objects.create(
        user=user,
        action='room_status_change',
        model_type='Room',
        object_id=room.id,
        description=f'Changed room {room.number} status from {old_status} to maintenance'
    )
    
    return Response({
        'message': 'Room marked for maintenance',
        'room_number': room.number,
        'old_status': old_status,
        'new_status': room.status
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def finish_room_maintenance(request, room_id):
    """
    Mark a room as available after maintenance
    """
    user = request.user
    
    # Only reception staff can finish room maintenance
    if not user.is_reception():
        return Response({
            'error': 'Only reception staff can finish room maintenance'
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        room = Room.objects.get(id=room_id)
    except Room.DoesNotExist:
        return Response({
            'error': 'Room not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Check if room is actually in maintenance
    if room.status != 'maintenance':
        return Response({
            'error': 'Room is not currently under maintenance'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Update room status
    old_status = room.status
    room.status = 'dispo'
    room.save()
    
    # Log the action
    AuditLog.objects.create(
        user=user,
        action='room_status_change',
        model_type='Room',
        object_id=room.id,
        description=f'Changed room {room.number} status from {old_status} to available (maintenance finished)'
    )
    
    return Response({
        'message': 'Room maintenance finished',
        'room_number': room.number,
        'old_status': old_status,
        'new_status': room.status
    })