"""
Main URL configuration for the Movie Theater Booking project.

This file connects:
- The Django admin panel
- The bookings app (UI + API routes)
- Authentication routes (login/logout)
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin panel
    path("admin/", admin.site.urls),

    # Bookings app (includes template pages and API endpoints)
    path("", include("bookings.urls")),

    
]