#from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
#from django.contrib.postgres.fields import JSONField  # If using PostgreSQL
#from django.contrib.postgres.fields import JSONField  # If using PostgreSQL


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    
    # Fix reverse accessor clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='booking_user_set',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.'
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='booking_user_set',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.'
    )

    def __str__(self):
        return self.username
    

class Train(models.Model):
    name = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    total_seats = models.IntegerField()
    available_seats = models.IntegerField()
    route = models.JSONField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id:  # New train
            self.available_seats = self.total_seats
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.source} -> {self.destination})"



class Seat(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.IntegerField()
    version = models.IntegerField(default=0)  # For optimistic locking
    source = models.CharField(max_length=100, blank=True, null=True)  # Source station for booking
    destination = models.CharField(max_length=100, blank=True, null=True)  # Destination station for booking

    @property
    def is_booked(self):
        return self.source is not None and self.destination is not None

    def book_seat(self, booking_source, booking_destination):
        """
        Book a seat for a specific segment if available.
        """
        if self._conflicts_with_existing_booking(booking_source, booking_destination):
            raise ValueError(f"Seat {self.seat_number} is not available for the requested route segment.")

        self.source = booking_source
        self.destination = booking_destination
        self.version = F('version') + 1  # Optimistic locking
        self.save()

    def _conflicts_with_existing_booking(self, booking_source, booking_destination):
        """
        Check if the requested booking conflicts with an existing booking.
        """
        if not self.source or not self.destination:
            return False  # No conflict if seat is not booked

        # Conflict if the ranges overlap
        return not (booking_destination <= self.source or booking_source >= self.destination)

    def __str__(self):
        return f"Seat {self.seat_number} on Train {self.train.name}"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    source = models.CharField(max_length=100, blank=True, null=False, default="Unknown")  # Default set here
    destination = models.CharField(max_length=100, blank=True, null=False, default="Unknown")  # Default set here
    booking_time = models.DateTimeField(auto_now_add=True)
    route = models.JSONField(blank=True, null=True)



# Create your models here.
