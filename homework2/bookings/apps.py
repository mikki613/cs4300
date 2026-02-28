"""
App configuration for the bookings app.

This connects the bookings app to the Django project
and allows Django to recognize it during startup.
"""

from django.apps import AppConfig


class BookingsConfig(AppConfig):
    """
    Configuration class for the bookings application.
    """
    name = "bookings"