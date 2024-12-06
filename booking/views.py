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
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        source = request.GET.get('source')
        destination = request.GET.get('destination')
        
        if not source or not destination:
            return JsonResponse({
                'error': 'Source and destination are required'
            }, status=400)
        
        trains = Train.objects.filter(
            source=source,
            destination=destination
        ).values('id', 'name', 'available_seats')
        
        return JsonResponse({
            'trains': list(trains)
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# User endpoint to book a seat
@csrf_exempt
def book_seat(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    data = json.loads(request.body)
    train_id = data.get('train_id')
    
    try:
        train = Train.objects.get(id=train_id)
    except Train.DoesNotExist:
        return JsonResponse({'error': 'Train not found'}, status=404)
    
    available_seat = Seat.objects.filter(train=train, is_booked=False).first()
    if not available_seat:
        return JsonResponse({'error': 'No available seats'}, status=400)
    
    # Optimistic locking to handle race conditions
    if available_seat.is_booked:
        return JsonResponse({"error": "Seat is already booked"}, status=400)

    rows_updated = Seat.objects.filter(
        pk=available_seat.pk,
        version=available_seat.version
    ).update(
        is_booked=True,
        version=F('version') + 1
    )
    
    if rows_updated == 0:
        return JsonResponse({"error": "Booking failed due to concurrent modification. Please try again."}, status=400)
    
    booking = Booking.objects.create(user=request.user, train=train, seat=available_seat)
    return JsonResponse({'message': 'Booking successful', 'booking_id': booking.id})

# User endpoint to get specific booking details
@csrf_exempt
def get_booking_details(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    booking_id = request.GET.get('booking_id')
    
    try:
        booking = Booking.objects.get(id=booking_id)
    except Booking.DoesNotExist:
        return JsonResponse({'error': 'Booking not found'}, status=404)
    
    return JsonResponse({
        'booking_id': booking.id,
        'train_id': booking.train.id,
        'seat_id': booking.seat.id,
        'status': 'Booked' if booking.seat.is_booked else 'Available'
    })