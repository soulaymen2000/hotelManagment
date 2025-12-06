from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages

@login_required
def reception_dashboard(request):
    """Reception dashboard view"""
    # Check if user is authenticated with session
    if not request.user.is_authenticated:
        messages.error(request, 'Please log in to access the reception dashboard.')
        return redirect('login')
    
    # Check if user has reception role
    if not request.user.is_reception():
        messages.error(request, 'You do not have permission to access the reception dashboard.')
        return redirect('home')
    
    return render(request, 'dashboard/reception_dashboard.html')

@login_required
def guest_dashboard(request):
    """Guest dashboard view"""
    # Check if user is authenticated with session
    if not request.user.is_authenticated:
        messages.error(request, 'Please log in to access the guest dashboard.')
        return redirect('login')
    
    # Check if user has guest role
    if not request.user.is_guest():
        messages.error(request, 'You do not have permission to access the guest dashboard.')
        return redirect('home')
    
    return render(request, 'dashboard/guest_dashboard.html')

@login_required
def admin_dashboard(request):
    """Admin dashboard view"""
    # Check if user is authenticated with session
    if not request.user.is_authenticated:
        messages.error(request, 'Please log in to access the admin dashboard.')
        return redirect('login')
    
    # Check if user has admin role
    if not request.user.is_admin():
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('home')
    
    return render(request, 'dashboard/admin_dashboard.html')