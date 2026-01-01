from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Profile
from .serializers import ProfileSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Login with email/username and return JWT tokens"""
    email = request.data.get('email') or request.data.get('username')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({'error': 'Email/username and password required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        profile = Profile.objects.get(email=email)
        user, created = User.objects.get_or_create(
            username=email,
            defaults={'email': email}
        )
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'profile': ProfileSerializer(profile).data
        })
        
    except Profile.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Register a new user profile"""
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({'error': 'Email and password required'}, status=status.HTTP_400_BAD_REQUEST)
    
    if Profile.objects.filter(email=email).exists():
        return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Create profile
    profile = Profile.objects.create(email=email, role='user')
    
    # Create Django user
    user = User.objects.create_user(username=email, email=email, password=password)
    
    refresh = RefreshToken.for_user(user)
    
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'profile': ProfileSerializer(profile).data
    }, status=status.HTTP_201_CREATED)