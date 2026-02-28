"""
URLs for the bookings app.

This file includes:
- UI pages (movie list, book seat page, booking history)
- Auth routes (login/logout/password reset) via Django's built-in auth URLs
- A signup page
- REST API routes (movies, seats, bookings) using DRF's router
"""

from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter

from . import views
from .views import MovieViewSet, SeatViewSet, BookingViewSet

# DRF router auto-creates /api/movies/, /api/seats/, /api/bookings/
router = DefaultRouter()
router.register(r"movies", MovieViewSet, basename="movie")
router.register(r"seats", SeatViewSet, basename="seat")
router.register(r"bookings", BookingViewSet, basename="booking")

urlpatterns = [
    # -------------------------
    # UI pages
    # -------------------------
    path("", views.movie_list_page, name="movie_list"),
    path("movies/<int:movie_id>/book/", views.seat_booking_page, name="book_seat"),
    path("history/", views.booking_history_page, name="booking_history"),

    # -------------------------
    # Authentication
    # -------------------------
    # This provides:
    # /accounts/login/, /accounts/logout/, /accounts/password_reset/, etc.
    path("accounts/", include("django.contrib.auth.urls")),
    # Custom signup
    path("accounts/signup/", views.signup, name="signup"),

    # -------------------------
    # API
    # -------------------------
    path("api/", include(router.urls)),
]