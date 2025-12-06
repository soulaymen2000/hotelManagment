from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


@login_required
def room_management(request):
    """Room management view for reception staff"""
    if not request.user.is_reception():
        return redirect('home')
    return render(request, 'rooms/room_management.html')


@login_required
def room_detail(request, room_id):
    """Room detail view"""
    # In a real application, you would fetch the room from the database
    # For now, we'll just render the template
    return render(request, 'rooms/room_detail.html')