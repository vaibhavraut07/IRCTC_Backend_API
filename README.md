# Railway Management System


This project is a Railway Management System, designed to allow users to register, login, check train availability, book seats, and get specific booking details. It also includes an admin interface to add trains and manage seat bookings. The system is optimized for handling concurrent seat bookings and includes role-based access control for admin operations.


## Features


- **User Registration & Login**: Allows users to register and login using JWT tokens.
- **Admin Features**: Admin users can add new trains, manage seat availability.
- **Seat Availability**: Users can check the available seats between two stations.
- **Seat Booking**: Users can book seats if available. Uses optimistic locking to handle race conditions.
- **Booking Details**: Users can view details of their booking.


## Tech Stack


- **Backend**: Django + Django REST Framework
- **Database**: PostgreSQL/MySQL
- **Authentication**: JWT (JSON Web Tokens)
- **Middleware**: API Key Middleware for admin access control
- **Concurrency**: Optimistic locking for seat booking


## Requirements


- Python 3.8+
- Django 3.x or higher
- PostgreSQL or MySQL database
- Django REST Framework
- `djangorestframework-simplejwt` for JWT authentication
### 1. Clone the repository

git clone https://github.com/yourusername/railway-management-system.git
cd railway-management-system


### 2\. Install dependencies

Create a virtual environment and install the necessary dependencies:

python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt


### 3\. Setup database

Make sure you have PostgreSQL or MySQL set up. Update the database configuration in settings.py:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # or mysql
        'NAME': 'railway_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',  # 3306 for MySQL
    }
}
  `

### 4\. Apply migrations

python manage.py migrate
  `

### 5\. Create a superuser (admin)

python manage.py createsuperuser
 `

### 6\. Start the Django development server

python manage.py runserver


The application should now be running at http://localhost:8000/.

API Endpoints
-------------

### User Registration

*   **POST /api/register/**
    
    *   jsonCopy code{ "username": "newuser", "password": "password123", "role": "user"}
        
    *   jsonCopy code{ "message": "Registration successful", "tokens": { "refresh": "refresh\_token\_here", "access": "access\_token\_here" }}
        

### User Login

*   **POST /api/login/**
    
    *   jsonCopy code{ "username": "existinguser", "password": "password123"}
        
    *   jsonCopy code{ "message": "Login successful", "tokens": { "refresh": "refresh\_token\_here", "access": "access\_token\_here" }}
        

### Add Train (Admin Only)

*   **POST /api/admin/add\_train/** (Requires API Key)
    
    *   Headers: X-API-KEY:
        
    *   jsonCopy code{ "source": "Station A", "destination": "Station B", "train\_number": "12345"}
        
    *   jsonCopy code{ "message": "Train added successfully"}
        

### Get Seat Availability

*   **GET /api/get\_seat\_availability/**
    
    *   Query Parameters: source=&destination=
        
    *   jsonCopy code{ "trains": \[ { "train\_id": 1, "available\_seats": 10 } \]}
        

### Book a Seat

*   **POST /api/book\_seat/**
    
    *   jsonCopy code{ "train\_id": 1}
        
    *   jsonCopy code{ "message": "Booking successful", "booking\_id": 123}
        

### Get Booking Details

*   **GET /api/get\_booking\_details/**
    
    *   Query Parameters: booking\_id=
        
    *   jsonCopy code{ "booking\_id": 123, "train\_id": 1, "seat\_id": 10, "status": "Booked"}
        

Middleware
----------

*   **Admin API Key Middleware**: Protects admin routes by requiring an API key (X-API-KEY header) to access endpoints such as /api/admin/add\_train/.
    
*   **JWT Authentication Middleware**: Ensures that users can only access certain endpoints if they are authenticated with a valid JWT token.
    

Optimistic Locking for Seat Booking
-----------------------------------

To handle race conditions when multiple users try to book the same seat at the same time, the system uses optimistic locking. This involves checking the version of the seat record before updating it. If another user has already booked the seat, the system will fail the booking attempt and prompt the user to try again.

Troubleshooting
---------------

1.  **Unauthorized Errors**: Make sure the X-API-KEY header is set correctly for admin routes, and the JWT token is provided in the Authorization header for user routes.
    
2.  **Database Errors**: Ensure the database is correctly configured in settings.py and migrations are applied.
    

License
-------

This project is licensed under the MIT License - see the LICENSE file for details.
```bash
### Key Sections of the README:
- **Project Overview**: A description of the system and its purpose.
- **Tech Stack**: Technologies used to build the project.
- **Setup Instructions**: Steps to set up the environment and run the project locally.
- **API Documentation**: Detailed descriptions of each API endpoint, including request bodies, headers, and responses.
- **Middleware**: Explanation of the API key and JWT middleware.
- **Optimistic Locking**: A description of how the race condition is handled during seat booking.
- **Troubleshooting**: Common issues and how to resolve them.

Let me know if you need further changes or additions to the README!

`



