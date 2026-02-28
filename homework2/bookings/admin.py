"""
Admin configuration for the bookings app.

This file registers the Movie, Seat, and Booking models
so they can be managed through the Django admin panel.
"""

from django.contrib import admin
from .models import Movie, Seat, Booking


"""
Register Movie model so movies can be added,
edited, and deleted from the admin interface.
"""
admin.site.register(Movie)


"""
Register Seat model so seat availability
can be managed through the admin panel.
"""
admin.site.register(Seat)


"""
Register Booking model so bookings can be viewed
and managed by administrators.
"""
admin.site.register(Booking)