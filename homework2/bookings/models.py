"""
Models for the Movie Theater Booking application.

These models represent movies, seats, and bookings
stored in the database.
"""

from django.conf import settings
from django.db import models


class Movie(models.Model):
    """
    Represents a movie that can be listed and booked.
    """

    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")

    def __str__(self) -> str:
        """Return the movie title when displayed in admin or shell."""
        return self.title


class Seat(models.Model):
    """
    Represents a seat in the theater.
    Tracks whether the seat has been booked.
    """

    seat_number = models.CharField(max_length=10, unique=True)
    is_booked = models.BooleanField(default=False)

    def __str__(self) -> str:
        """Return the seat number for display purposes."""
        return self.seat_number


class Booking(models.Model):
    """
    Represents a booking made by a user for a specific movie and seat.
    Each seat can only have one booking.
    """

    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    seat = models.OneToOneField(
        Seat,
        on_delete=models.PROTECT,
        related_name="booking"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Return a readable description of the booking."""
        return f"{self.user} booked {self.seat} for {self.movie}"