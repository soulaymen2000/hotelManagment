from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from .serializers import UserSerializer, UserRegistrationSerializer, UserUpdateSerializer
from audit.models import AuditLog
import logging

# Set up logging
logger = logging.getLogger(__name__)

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        logger.info("User registration request received")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Log the action
            AuditLog.objects.create(
                user=user,
                action='create',
                model_type='User',
                object_id=user.id,
                description=f'User {user.email} registered'
            )
            
            logger.info(f"User {user.email} registered successfully")
            return Response({
                'message': 'User registered successfully',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        logger.warning(f"User registration failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        logger.info("Login request received")
        logger.info(f"Request data: {request.data}")
        logger.info(f"Request headers: {dict(request.headers)}")
        logger.info(f"Content type: {request.content_type}")
        
        try:
            response = super().post(request, *args, **kwargs)
            logger.info(f"JWT response status: {response.status_code}")
            
            if response.status_code == status.HTTP_200_OK:
                try:
                    # Get the user from the request
                    email = request.data.get('email')
                    logger.info(f"Looking up user with email: {email}")
                    user = User.objects.get(email=email)
                    
                    # Add user role to the response
                    response.data['user_role'] = user.role
                    logger.info(f"Added user role {user.role} to response")
                    
                    # Add payload field for frontend compatibility
                    response.data['payload'] = {
                        'access': response.data['access'],
                        'refresh': response.data['refresh'],
                        'user_role': user.role
                    }
                    logger.info("Added payload field for frontend compatibility")
                    
                    # Log the action
                    AuditLog.objects.create(
                        user=user,
                        action='login',
                        model_type='User',
                        object_id=user.id,
                        description=f'User {user.email} logged in'
                    )
                    logger.info(f"Logged login action for user {user.email}")
                except User.DoesNotExist:
                    logger.error(f"User with email {email} does not exist")
                    # If user doesn't exist, we still return the token but without user_role
                    # This shouldn't happen in normal circumstances since JWT authentication
                    # should have already validated the credentials
                    # Add payload field even in error case
                    response.data['payload'] = {
                        'access': response.data.get('access', ''),
                        'refresh': response.data.get('refresh', ''),
                        'user_role': 'guest'
                    }
                except Exception as e:
                    logger.error(f"Error during login processing: {str(e)}", exc_info=True)
                    # Add payload field even in error case
                    response.data['payload'] = {
                        'access': response.data.get('access', ''),
                        'refresh': response.data.get('refresh', ''),
                        'user_role': 'guest'
                    }
            
            logger.info(f"Returning response with data keys: {list(response.data.keys()) if hasattr(response, 'data') else 'No data'}")
            logger.info(f"Response data: {response.data if hasattr(response, 'data') else 'No data'}")
            return response
        except Exception as e:
            logger.error(f"Exception in login view: {str(e)}", exc_info=True)
            raise


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        old_email = user.email
        
        response = super().update(request, *args, **kwargs)
        
        # Log the action
        AuditLog.objects.create(
            user=user,
            action='update',
            model_type='User',
            object_id=user.id,
            description=f'User {old_email} updated their profile'
        )
        
        return response


# Admin-only views
class AdminUserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    
    def get_queryset(self):
        # Only admin users can list all users
        if self.request.user.is_admin():
            return User.objects.all()
        return User.objects.none()


class AdminUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    
    def get_permissions(self):
        # Only admin users can access this view
        if not self.request.user.is_admin():
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        old_role = user.role
        
        # Handle partial updates (PATCH) for role changes
        if 'role' in request.data and len(request.data) == 1:
            # Only role is being updated
            user.role = request.data['role']
            user.save(update_fields=['role'])
            
            # Serialize the updated user
            serializer = self.get_serializer(user)
            
            # Log the action
            AuditLog.objects.create(
                user=self.request.user,
                action='update',
                model_type='User',
                object_id=user.id,
                description=f'Admin updated user {user.email} role from {old_role} to {user.role}'
            )
            
            return Response(serializer.data)
        else:
            # Handle full updates
            response = super().update(request, *args, **kwargs)
            
            # Log the action
            AuditLog.objects.create(
                user=self.request.user,
                action='update',
                model_type='User',
                object_id=user.id,
                description=f'Admin updated user {user.email} role from {old_role} to {user.role}'
            )
            
            return response
    
    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        
        # Prevent admin users from deleting other admins
        if user.is_admin() and user != self.request.user:
            return Response({
                'error': 'Cannot delete another admin user'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Prevent users from deleting themselves
        if user == self.request.user:
            return Response({
                'error': 'Cannot delete your own account'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        response = super().destroy(request, *args, **kwargs)
        
        # Log the action
        AuditLog.objects.create(
            user=self.request.user,
            action='delete',
            model_type='User',
            object_id=user.id,
            description=f'Admin deleted user {user.email}'
        )
        
        return response