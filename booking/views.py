import json
import logging
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate
from .models import User, Train, Seat, Booking
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.db.models import F
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction
from django.contrib.auth.decorators import login_required


logger = logging.getLogger(__name__)

@csrf_exempt
def register_user(request):
    if request.method != 'POST':
        logger.error("Method not allowed, only POST is allowed.")
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    logger.info("Register API triggered")
    try:
        # Parse JSON data from request body
        data = json.loads(request.body)
        logger.info(f"Received data: {data}")

        # Validate required fields
        if 'username' not in data or 'password' not in data:
            logger.error("Missing 'username' or 'password' in the request")
            return JsonResponse({'error': 'Username and password are required'}, status=400)
         
        # Create the user
        user = User.objects.create_user(
            username=data['username'],
            password=data['password'],
            role=data.get('role', 'user'),
            is_active=True
        )

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return JsonResponse({
            'message': 'Registration successful',
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
        }, status=201)

    except json.JSONDecodeError:
        logger.error("Invalid JSON data received")
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    except Exception as e:
        logger.error(f"Error occurred during registration: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)

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


@csrf_exempt
def add_train(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        
        # Create train
        train = Train.objects.create(
            name=data['name'],
            source=data['source'],
            destination=data['destination'],
            total_seats=data['total_seats'],
            available_seats=data['total_seats']
        )
        
        return JsonResponse({
            'message': 'Train added successfully',
            'train': {
                'id': train.id,
                'name': train.name,
                'source': train.source,
                'destination': train.destination,
                'total_seats': train.total_seats
            }
        }, status=201)
    
    except KeyError as e:
        return JsonResponse({'error': f"Missing field: {str(e)}"}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def get_seat_availability(request):
    if request.method != 'GET':
        logger.error("Method not allowed in get_seat_availability")
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        # Get and validate parameters
        data = request.GET
        if 'source' not in data or 'destination' not in data:
            return JsonResponse({'error': 'Source and destination are required'}, status=400)

        source = data['source']
        destination = data['destination']
        
        # Query trains
        trains = Train.objects.filter(source=source, destination=destination)
        
        # Format response
        trains_data = [{
            'id': train.id,
            'name': train.name,
            'source': train.source,
            'destination': train.destination,
            'available_seats': train.available_seats,
            'total_seats': train.total_seats
        } for train in trains]
        
        return JsonResponse({'trains': trains_data})

    except Exception as e:
        logger.error(f"Error in get_seat_availability: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@login_required
@transaction.atomic
@csrf_exempt
@login_required
@transaction.atomic
def book_seat(request):
    if request.method != 'POST':
        logger.error("Method not allowed")
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        logger.info("Booking seat request received")
        # Verify authenticated user
        if not request.user.is_authenticated:
            logger.error("User not authenticated")
            return JsonResponse({'error': 'Authentication required'}, status=401)
            
        # Parse JSON data
        data = json.loads(request.body)
        logger.info(f"Request data: {data}")
        
        if 'train_id' not in data:
            logger.error("Missing train_id")
            return JsonResponse({'error': 'Train ID is required'}, status=400)
            
        train_id = data['train_id']
        
        # Get train with lock
        train = Train.objects.select_for_update().get(id=train_id)
        logger.info(f"Train found: {train.name}")

        if train.available_seats <= 0:
            logger.error(f"No seats available for train {train.name}")
            return JsonResponse({'error': 'No seats available'}, status=400)
            
        # Book seat
        train.available_seats -= 1
        train.save()

        # Create booking
        booking = Booking.objects.create(
            user=request.user,
            train=train
        )
        
        return JsonResponse({
            'message': 'Booking successful',
            'booking': {
                'id': booking.id,
                'train_name': train.name,
                'source': train.source,
                'destination': train.destination
            }
        })

    except Train.DoesNotExist:
        logger.error(f"Train with ID {train_id} does not exist")
        return JsonResponse({'error': 'Train not found'}, status=404)
    except Exception as e:
        logger.error(f"Error in booking: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def get_booking_details(request):
    if request.method != 'GET':
        logger.error("Method not allowed in get_booking_details")
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        # Get and validate parameters
        booking_id = request.GET.get('booking_id')
        if not booking_id:
            return JsonResponse({'error': 'Booking ID is required'}, status=400)
            
        # Get booking
        booking = Booking.objects.get(id=booking_id)
        
        # Format response
        return JsonResponse({
            'booking': {
                'id': booking.id,
                'train_name': booking.train.name,
                'source': booking.train.source,
                'destination': booking.train.destination,
                'booking_time': booking.booking_time
            }
        })

    except Booking.DoesNotExist:
        return JsonResponse({'error': 'Booking not found'}, status=404)
    except Exception as e:
        logger.error(f"Error in get_booking_details: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)