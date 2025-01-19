from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

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
    is_booked = models.BooleanField(default=False)
    source = models.CharField(max_length=100, blank=True, null=True)
    destination = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Seat {self.seat_number} on Train {self.train.name}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    booking_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} by {self.user.username}"