from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .models import Seat

DEFAULT_SEAT_COUNT = 30


@receiver(post_migrate)
def create_default_seats(sender, **kwargs):
    """
    Ensure the database has seats after migrations.
    """
    if getattr(sender, "name", None) != "bookings":
        return

    if Seat.objects.exists():
        return

    seats = [Seat(seat_number=f"A{i}") for i in range(1, DEFAULT_SEAT_COUNT + 1)]
    Seat.objects.bulk_create(seats)