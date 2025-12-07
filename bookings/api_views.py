from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Booking
from .serializers import BookingSerializer, BookingCreateSerializer, BookingStatusUpdateSerializer
from rooms.models import Room
from accounts.models import User
from audit.models import AuditLog


class GuestBookingCreateView(generics.CreateAPIView):
    serializer_class = BookingCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        # Set the guest to the current user
        booking = serializer.save(guest=self.request.user)
        
        # Update room status to reserved
        room = booking.room
        room.status = 'reserved'
        room.save()
        
        # Log the action
        AuditLog.objects.create(
            user=self.request.user,
            action='create',
            model_type='Booking',
            object_id=booking.id,
            description=f'Created booking for room {room.number}'
        )
        
        # Also log room status change
        AuditLog.objects.create(
            user=self.request.user,
            action='room_status_change',
            model_type='Room',
            object_id=room.id,
            description=f'Changed room {room.number} status to reserved'
        )


class GuestBookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Guests can only see their own bookings
        return Booking.objects.filter(guest=self.request.user)


class ReceptionBookingListView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Reception staff can see all bookings
        if self.request.user.is_reception():
            return Booking.objects.all()
        return Booking.objects.none()


class ReceptionBookingCreateView(generics.CreateAPIView):
    serializer_class = BookingCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        if not request.user.is_reception() and not request.user.is_admin():
            return Response({
                'error': 'Only reception staff can create bookings'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Get guest email from request data
        guest_email = request.data.get('guest_email')
        if not guest_email:
            return Response({
                'error': 'Guest email is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Try to find existing user or return error
        try:
            guest = User.objects.get(email=guest_email)
        except User.DoesNotExist:
            return Response({
                'error': f'No user found with email {guest_email}. Please register the guest first.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Store guest for perform_create
        self.guest = guest
        
        return super().create(request, *args, **kwargs)
        
    def perform_create(self, serializer):
        # Save with confirmed status for reception bookings
        booking = serializer.save(guest=self.guest, status='confirmed')
        
        # Update room status to booked
        room = booking.room
        room.status = 'booked'
        room.save()
        
        # Log the actions
        AuditLog.objects.create(
            user=self.request.user,
            action='create',
            model_type='Booking',
            object_id=booking.id,
            description=f'Reception created booking for room {booking.room.number}'
        )
        
        AuditLog.objects.create(
            user=self.request.user,
            action='room_status_change',
            model_type='Room',
            object_id=room.id,
            description=f'Changed room {room.number} status to booked'
        )


class ReceptionBookingStatusUpdateView(generics.UpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingStatusUpdateSerializer
    permission_classes = [IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        if not request.user.is_reception():
            return Response({
                'error': 'Only reception staff can update booking status'
            }, status=status.HTTP_403_FORBIDDEN)
            
        booking = self.get_object()
        old_status = booking.status
        response = super().update(request, *args, **kwargs)
        
        # If status changed to 'checked_in', update room status
        if booking.status == 'checked_in' and old_status != 'checked_in':
            room = booking.room
            room.status = 'booked'
            room.save()
            
            # Log room status change
            AuditLog.objects.create(
                user=request.user,
                action='room_status_change',
                model_type='Room',
                object_id=room.id,
                description=f'Changed room {room.number} status to booked (check-in)'
            )
            
        # If status changed to 'checked_out', update room status
        elif booking.status == 'checked_out' and old_status != 'checked_out':
            room = booking.room
            room.status = 'dispo'
            room.save()
            
            # Log room status change
            AuditLog.objects.create(
                user=request.user,
                action='room_status_change',
                model_type='Room',
                object_id=room.id,
                description=f'Changed room {room.number} status to available (check-out)'
            )
            
        # Log booking status change
        AuditLog.objects.create(
            user=request.user,
            action='booking_status_change',
            model_type='Booking',
            object_id=booking.id,
            description=f'Changed booking status from {old_status} to {booking.status}'
        )
        
        return response


class ReceptionBookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        if not request.user.is_reception():
            return Response({
                'error': 'Only reception staff can update bookings'
            }, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
        
    def destroy(self, request, *args, **kwargs):
        if not request.user.is_reception():
            return Response({
                'error': 'Only reception staff can delete bookings'
            }, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)