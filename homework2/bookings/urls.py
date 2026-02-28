"""
URLs for the bookings app.

This file includes:
- UI pages (movie list, seat booking, booking history)
- Auth pages (login/logout/password reset) via Django's built-in auth URLs
- A custom signup route
- REST API endpoints (DRF router)
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import MovieViewSet, SeatViewSet, BookingViewSet

# DRF router for API endpoints
router = DefaultRouter()
router.register(r"movies", MovieViewSet)
router.register(r"seats", SeatViewSet)
router.register(r"bookings", BookingViewSet)

urlpatterns = [
    # -------------------
    # UI pages
    # -------------------
    path("", views.movie_list_page, name="movie_list"),
    path("movies/<int:movie_id>/book/", views.seat_booking_page, name="book_seat"),
    path("history/", views.booking_history_page, name="booking_history"),

    # -------------------
    # Auth (login/logout/etc.)
    # This provides:
    # /accounts/login/
    # /accounts/logout/
    # /accounts/password_reset/
    # etc.
    # -------------------
    path("accounts/", include("django.contrib.auth.urls")),

    # Custom signup page
    path("accounts/signup/", views.signup, name="signup"),

    # -------------------
    # API routes
    # -------------------
    path("api/", include(router.urls)),
]