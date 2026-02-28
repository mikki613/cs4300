from django.conf import settings
from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField()
    duration_minutes = models.PositiveIntegerField()

    def __str__(self):
        return self.title


class Seat(models.Model):
    seat_number = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.seat_number


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    # IMPORTANT: this must NOT be OneToOne, or seats become globally single-use.
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name="bookings")
    booking_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            # Prevent same seat being booked twice for the SAME movie
            models.UniqueConstraint(fields=["movie", "seat"], name="unique_seat_per_movie"),
            # Prevent same user booking same seat for same movie twice (optional but nice)
            models.UniqueConstraint(fields=["user", "movie", "seat"], name="unique_user_movie_seat"),
        ]

    def __str__(self):
        return f"{self.user} booked {self.seat} for {self.movie}"