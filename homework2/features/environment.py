import os
import django

def before_all(context):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movie_theater_booking.settings")
    django.setup()