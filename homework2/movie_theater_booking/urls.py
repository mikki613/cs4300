"""
Main URL configuration for the Movie Theater Booking project.

- admin/ is the Django admin
- everything else is handled by the bookings app
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("bookings.urls")),
]