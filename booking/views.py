import json
import logging
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# from django.shortcuts import render
# from rest_framework import APIView
from django.http import JsonResponse
# from rest_framework.response import Response
# from .models import User
# from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken
# from .serializers import UserRegistrationSerializer, UserLoginSerializer
# from django.contrib.auth import authenticate

logger = logging.getLogger(__name__)
@csrf_exempt
def register_user(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        # Parse JSON data from request body
        data = json.loads(request.body)
        
        # Validate required fields
        if 'username' not in data or 'password' not in data:
            return JsonResponse({
                'error': 'Username and password are required'
            }, status=400)
            
        user = User.objects.create_user(
            username=data['username'],
            password=data['password'],
            role=data.get('role', 'user'),
            is_active=True
        )
        
        refresh = RefreshToken.for_user(user)
        return JsonResponse({
            'message': 'Registration successful',
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=400)

@csrf_exempt
def login_user(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        
        username = data.get('username')
        password = data.get('password')
        
        # Debug logging
        logger.info(f"Login attempt for username: {username}")
        
        # Check if user exists
        user = User.objects.filter(username=username).first()
        if not user:
            logger.error(f"User not found: {username}")
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
        
        logger.info(f"Found user: {user.username}, is_active: {user.is_active}")
        
        # Try authentication
        authenticated_user = authenticate(
            request=request,
            username=username,
            password=password
        )
        
        if authenticated_user is None:
            logger.error(f"Authentication failed for user: {username}")
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
        
        logger.info(f"Authentication successful for user: {username}")
        
        # Generate tokens
        refresh = RefreshToken.for_user(authenticated_user)
        
        return JsonResponse({
            'message': 'Login successful',
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
        })
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)


def add_train(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        # Example of adding a new train, assuming the API key is validated by middleware
        source = request.POST['source']
        destination = request.POST['destination']
        train_number = request.POST['train_number']

        train = Train.objects.create(
            source=source,
            destination=destination,
            train_number=train_number
        )

        return JsonResponse({'message': 'Train added successfully'}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)