"""
Behave environment configuration.

This file sets up Django before running any Behave tests.
It ensures the Django settings are loaded so models and
database access work correctly inside step definitions.
"""

import os
import django


def before_all(context):
    """
    Configure Django settings before running Behave tests.
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movie_theater_booking.settings")
    django.setup()