from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Room
from .serializers import RoomSerializer, RoomStatusUpdateSerializer
from accounts.models import User
from audit.models import AuditLog


class RoomListView(generics.ListAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        queryset = Room.objects.all()
        
        # Filter by availability if dates are provided
        check_in = self.request.query_params.get('check_in_date')
        check_out = self.request.query_params.get('check_out_date')
        
        if check_in and check_out:
            # Exclude rooms that have overlapping confirmed/checked_in bookings
            from django.db.models import Q
            queryset = queryset.exclude(
                bookings__status__in=['confirmed', 'checked_in'],
                bookings__check_in_date__lt=check_out,
                bookings__check_out_date__gt=check_in
            )
            
        return queryset


class RoomDetailView(generics.RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]


class ReceptionRoomListView(generics.ListCreateAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        # Only reception staff can manage rooms
        if user.is_reception():
            return Room.objects.all()
        return Room.objects.none()


class ReceptionRoomStatusUpdateView(generics.UpdateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomStatusUpdateSerializer
    permission_classes = [IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        user = self.request.user
        # Only reception staff can update room status
        if not user.is_reception():
            return Response({
                'error': 'Only reception staff can update room status'
            }, status=status.HTTP_403_FORBIDDEN)
            
        return super().update(request, *args, **kwargs)


class AdminRoomListView(generics.ListCreateAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        # Only admin users can manage rooms
        if user.is_admin():
            return Room.objects.all()
        return Room.objects.none()