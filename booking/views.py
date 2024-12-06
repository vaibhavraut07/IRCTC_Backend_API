from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
# from django.shortcuts import render
# from rest_framework import APIView
# from django.http import JsonResponse
# from rest_framework.response import Response
# from .models import User
# from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken
# from .serializers import UserRegistrationSerializer, UserLoginSerializer
# from django.contrib.auth import authenticate

def register_user(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    data = request.POST
    try:
        user = User.objects.create_user(
            username=data['username'],
            password=data['password'],
            role=data.get('role', 'user')
        )
        refresh = RefreshToken.for_user(user)
        
        return JsonResponse({
            'message': 'Registration successful',
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
        }, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def login_user(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    data = request.POST
    user = authenticate(
        username=data.get('username'),
        password=data.get('password')
    )
    
    if user:
        refresh = RefreshToken.for_user(user)
        return JsonResponse({
            'message': 'Login successful',
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
        })
    
    return JsonResponse({'error': 'Invalid credentials'}, status=401)


