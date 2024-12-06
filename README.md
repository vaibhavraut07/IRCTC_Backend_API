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
- PostgreSQL
- Django REST Framework
- `djangorestframework-simplejwt` for JWT authentication

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/railway-management-system.git
cd railway-management-system
