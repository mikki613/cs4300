"""
URL configuration for the bookings app.

This file connects:
- Template (UI) pages
- Authentication routes (login/logout)
- REST API endpoints using Django REST Framework
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    MovieViewSet,
    SeatViewSet,
    BookingViewSet,
    movie_list_page,
    seat_booking_page,
    booking_history_page,
)

# Router automatically generates API routes for our ViewSets
router = DefaultRouter()
router.register(r"movies", MovieViewSet)
router.register(r"seats", SeatViewSet)
router.register(r"bookings", BookingViewSet)

urlpatterns = [
    # -------------------------
    # Template Pages (UI)
    # -------------------------
    path("", movie_list_page, name="movie_list"),
    path("movies/<int:movie_id>/book/", seat_booking_page, name="book_seat"),
    path("history/", booking_history_page, name="booking_history"),

    # -------------------------
    # Authentication (Login/Logout)
    # -------------------------
    path("accounts/", include("django.contrib.auth.urls")),

    # -------------------------
    # REST API
    # -------------------------
    path("api/", include(router.urls)),
]