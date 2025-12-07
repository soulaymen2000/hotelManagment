from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from .models import User
import json
import logging

# Set up logging
logger = logging.getLogger(__name__)

@csrf_exempt
def login_view(request):
    """User login view"""
    logger.info("Template login view accessed")
    logger.info(f"Request method: {request.method}")
    logger.info(f"User authenticated: {request.user.is_authenticated}")
    
    if request.user.is_authenticated:
        # Redirect based on user role
        logger.info(f"User already authenticated: {request.user.email} with role {request.user.role}")
        if request.user.is_admin():
            return redirect('admin-dashboard')
        elif request.user.is_reception():
            return redirect('reception-dashboard')
        else:
            return redirect('guest-dashboard')
    
    if request.method == 'POST':
        logger.info("Processing POST login request")
        logger.info(f"Request content type: {request.content_type}")
        logger.info(f"Request body: {request.body}")
        logger.info(f"Request POST data: {request.POST}")
        
        try:
            # Parse JSON data from fetch request
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            logger.info(f"Parsed JSON data - Email: {email}")
        except Exception as e:
            logger.info("Not JSON data, using form data")
            # Handle form data from traditional POST
            email = request.POST.get('email')
            password = request.POST.get('password')
            logger.info(f"Form data - Email: {email}")
        
        if email and password:
            logger.info(f"Attempting authentication for email: {email}")
            user = authenticate(email=email, password=password)
            logger.info(f"Authentication result: {'Success' if user else 'Failed'}")
            
            if user:
                login(request, user)
                logger.info(f"User {user.email} logged in successfully")
                # Return JSON response for AJAX requests
                if request.content_type == 'application/json':
                    logger.info("Returning JSON response for AJAX request")
                    # Determine the correct redirect URL based on user role
                    if user.is_admin():
                        redirect_url = '/dashboards/admin/'
                    elif user.is_reception():
                        redirect_url = '/dashboards/reception/'
                    else:  # guest
                        redirect_url = '/dashboards/guest/'
                        
                    return JsonResponse({
                        'success': True,
                        'redirect_url': redirect_url,
                        'user_role': user.role,
                        'csrf_token': get_token(request)
                    })
                # Redirect for traditional form submissions
                else:
                    logger.info("Returning redirect response for form submission")
                    if user.is_admin():
                        return redirect('admin-dashboard')
                    elif user.is_reception():
                        return redirect('reception-dashboard')
                    else:
                        return redirect('guest-dashboard')
            else:
                logger.warning(f"Invalid credentials for email: {email}")
                # Return JSON response for AJAX requests
                if request.content_type == 'application/json':
                    return JsonResponse({
                        'success': False,
                        'error': 'Invalid credentials'
                    })
                # Add message for traditional form submissions
                else:
                    messages.error(request, 'Invalid credentials')
                    return render(request, 'registration/login.html')
        else:
            logger.warning("Email and password are required")
            # Return JSON response for AJAX requests
            if request.content_type == 'application/json':
                return JsonResponse({
                    'success': False,
                    'error': 'Email and password are required'
                })
            # Add message for traditional form submissions
            else:
                messages.error(request, 'Email and password are required')
                return render(request, 'registration/login.html')
    
    logger.info("Rendering login template")
    return render(request, 'registration/login.html')


@csrf_exempt
def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        try:
            # Parse JSON data
            data = json.loads(request.body)
            
            # Extract fields
            username = data.get('username')
            email = data.get('email')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            phone_number = data.get('phone_number', '')
            password = data.get('password')
            password_confirm = data.get('password_confirm')
            
            # Validate required fields
            if not all([username, email, first_name, last_name, password, password_confirm]):
                return JsonResponse({
                    'detail': 'All required fields must be filled'
                }, status=400)
            
            # Validate passwords match
            if password != password_confirm:
                return JsonResponse({
                    'password': ['Passwords do not match']
                }, status=400)
            
            # Check if user already exists
            if User.objects.filter(email=email).exists():
                return JsonResponse({
                    'email': ['A user with this email already exists']
                }, status=400)
            
            if User.objects.filter(username=username).exists():
                return JsonResponse({
                   'username': ['A user with this username already exists']
                }, status=400)
            
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                role='guest'  # Default role for registration
            )
            
            logger.info(f"New user registered: {user.email}")
            
            return JsonResponse({
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role
                },
                'message': 'Registration successful'
            }, status=201)
            
        except json.JSONDecodeError:
            return JsonResponse({
                'detail': 'Invalid JSON data'
            }, status=400)
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            return JsonResponse({
                'detail': f'Registration failed: {str(e)}'
            }, status=500)
    
    return render(request, 'registration/register.html')


@login_required
def profile_view(request):
    """User profile view"""
    return render(request, 'registration/profile.html')