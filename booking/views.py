import json
import logging
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import User, Train, Seat, Booking

logger = logging.getLogger(__name__)

@csrf_exempt
def register_user(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)
        if 'username' not in data or 'password' not in data:
            return JsonResponse({'error': 'Username and password are required'}, status=400)

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
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def login_user(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = User.objects.filter(username=username).first()
        if not user:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

        authenticated_user = authenticate(request=request, username=username, password=password)
        if authenticated_user is None:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

        refresh = RefreshToken.for_user(authenticated_user)
        return JsonResponse({
            'message': 'Login successful',
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
        })

    except Exception as e:
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
            available_seats=data['total_seats'],
            route=data.get('route', [])
        )

        # Log the train creation
        logger.info(f"Train created: {train.name} (ID: {train.id})")

        # Create seats for the train
        for seat_number in range(1, train.total_seats + 1):
            Seat.objects.create(train=train, seat_number=seat_number)
            logger.info(f"Seat {seat_number} created for train {train.name}")

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
        logger.error(f"Missing field: {str(e)}")
        return JsonResponse({'error': f"Missing field: {str(e)}"}, status=400)
    except Exception as e:
        logger.error(f"Error in add_train: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
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

        # Log the query parameters
        logger.info(f"Fetching trains for source: {source}, destination: {destination}")

        # Query all trains
        trains = Train.objects.all()
        available_trains = []

        for train in trains:
            # Check if the train has a route
            if not train.route:
                continue

            # Convert route to a list if it's stored as a string
            route = train.route if isinstance(train.route, list) else train.route.split(',')

            # Check if source and destination are in the route
            if source in route and destination in route:
                # Ensure source comes before destination in the route
                if route.index(source) < route.index(destination):
                    available_trains.append({
                        'id': train.id,
                        'name': train.name,
                        'source': source,
                        'destination': destination,
                        'available_seats': train.available_seats,
                        'total_seats': train.total_seats
                    })

        # Log the number of trains found
        logger.info(f"Found {len(available_trains)} trains")

        return JsonResponse({'trains': available_trains})

    except Exception as e:
        logger.error(f"Error in get_seat_availability: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
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

        # Validate required fields
        train_id = data.get('train_id')
        source = data.get('source')
        destination = data.get('destination')

        if not all([train_id, source, destination]):
            logger.error("Missing train_id, source, or destination")
            return JsonResponse({'error': 'Train ID, source, and destination are required'}, status=400)

        # Fetch train with lock
        train = Train.objects.select_for_update().get(id=train_id)
        logger.info(f"Train found: {train.name}")

        # Check if source and destination are in the route
        route = train.route if isinstance(train.route, list) else train.route.split(',')
        logger.info(f"Train route: {route}")

        if source not in route or destination not in route:
            logger.error(f"Source or destination not in route: source={source}, destination={destination}")
            return JsonResponse({'error': 'Invalid source or destination for the selected train'}, status=400)

        if route.index(source) >= route.index(destination):
            logger.error(f"Invalid order: source={source}, destination={destination}")
            return JsonResponse({'error': 'Invalid source or destination for the selected train'}, status=400)

        # Check for available seats
        available_seat = Seat.objects.filter(train=train, is_booked=False).first()
        if not available_seat:
            logger.error("No seats available")
            return JsonResponse({'error': 'No available seats for the selected train'}, status=400)

        # Book the seat
        available_seat.is_booked = True
        available_seat.source = source  # Update source
        available_seat.destination = destination  # Update destination
        available_seat.save()

        # Create the booking
        booking = Booking.objects.create(
            user=request.user,
            train=train,
            seat=available_seat,
            source=source,
            destination=destination
        )

        # Decrease available seats count for the train
        train.available_seats -= 1
        train.save()

        logger.info(f"Booking successful for user {request.user.username}")
        return JsonResponse({
            'message': 'Booking successful',
            'booking': {
                'id': booking.id,
                'train_name': train.name,
                'source': source,
                'destination': destination,
                'seat_id': available_seat.id
            }
        })

    except Train.DoesNotExist:
        logger.error(f"Train with ID {train_id} does not exist")
        return JsonResponse({'error': 'Train not found'}, status=404)
    except Exception as e:
        logger.error(f"Error in booking: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_booking_details(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        booking_id = request.GET.get('booking_id')
        if not booking_id:
            return JsonResponse({'error': 'Booking ID is required'}, status=400)

        booking = Booking.objects.get(id=booking_id)
        if booking.user != request.user:
            return JsonResponse({'error': 'Unauthorized'}, status=403)

        return JsonResponse({
            'booking': {
                'id': booking.id,
                'train_name': booking.train.name,
                'source': booking.source,
                'destination': booking.destination,
                'booking_time': booking.booking_time
            }
        })

    except Booking.DoesNotExist:
        return JsonResponse({'error': 'Booking not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)