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
        return self.title


class Seat(models.Model):
    """
    Represents a seat in the theater.
    """

    seat_number = models.CharField(max_length=10, unique=True)

    def __str__(self) -> str:
        return self.seat_number


class Booking(models.Model):
    """
    Represents a booking made by a user for a specific movie and seat.

    A seat can be booked for different movies, but only once per movie.
    """

    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="bookings",
    )

    # IMPORTANT CHANGE: this must be ForeignKey (NOT OneToOneField)
    seat = models.ForeignKey(
        Seat,
        on_delete=models.PROTECT,
        related_name="bookings",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings",
    )

    booking_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["movie", "seat"],
                name="unique_seat_per_movie",
            )
        ]

    def __str__(self) -> str:
        return f"{self.user} booked {self.seat} for {self.movie}"