"""
Signal handlers for the bookings app.

This module ensures that default seats are created automatically
after database migrations are applied.
"""

from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .models import Seat

DEFAULT_SEAT_COUNT = 30


@receiver(post_migrate)
def ensure_default_seats(sender, **kwargs):

    """
    Creates default seats after migrations run.

    If fewer than DEFAULT_SEAT_COUNT seats exist,
    the missing seats will be created automatically.
    """
    
    # Only run this for the bookings app
    if getattr(sender, "name", None) != "bookings":
        return

    # Get all existing seat numbers
    existing = set(Seat.objects.values_list("seat_number", flat=True))
    
    # Determine which seats are missing
    missing = [
        Seat(seat_number=f"A{i}")
        for i in range(1, DEFAULT_SEAT_COUNT + 1)
        if f"A{i}" not in existing
    ]
    

    # Create only the seats that do not already exist
    if missing:
        Seat.objects.bulk_create(missing)