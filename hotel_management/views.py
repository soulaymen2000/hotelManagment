from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def home(request):
    # If user is authenticated, redirect to their dashboard
    if request.user.is_authenticated:
        if request.user.is_admin():
            return redirect('admin-dashboard')
        elif request.user.is_reception():
            return redirect('reception-dashboard')
        else:
            return redirect('guest-dashboard')
    # Otherwise, show the home page with login option
    return render(request, 'index.html')

def test_layout(request):
    """Render the test layout page"""
    return render(request, 'test_layout.html')

@login_required
def dashboard_redirect(request):
    """Redirect users to their appropriate dashboard"""
    # Check if user is authenticated with session
    if not request.user.is_authenticated:
        messages.error(request, 'Please log in to access your dashboard.')
        return redirect('login')
    
    if request.user.is_admin():
        return redirect('admin-dashboard')
    elif request.user.is_reception():
        return redirect('reception-dashboard')
    else:
        return redirect('guest-dashboard')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')