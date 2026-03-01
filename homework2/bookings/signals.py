from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .models import Seat

DEFAULT_SEAT_COUNT = 30


@receiver(post_migrate)
def ensure_default_seats(sender, **kwargs):
    """
    Ensure the database has at least DEFAULT_SEAT_COUNT seats after migrations.

    If some seats already exist (e.g., 10), this will create the missing ones
    instead of doing nothing.
    """
    if getattr(sender, "name", None) != "bookings":
        return

    existing = set(Seat.objects.values_list("seat_number", flat=True))

    missing = [
        Seat(seat_number=f"A{i}")
        for i in range(1, DEFAULT_SEAT_COUNT + 1)
        if f"A{i}" not in existing
    ]

    if missing:
        Seat.objects.bulk_create(missing)