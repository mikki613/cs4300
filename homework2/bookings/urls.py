"""
URL configuration for the bookings app.

This file connects:
- Template (UI) pages (movie list, booking seats, booking history)
- Authentication routes (login/logout/signup)
- REST API endpoints using Django REST Framework routers
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views

from . import views
from .views import MovieViewSet, SeatViewSet, BookingViewSet


# -------------------------
# REST API ROUTER
# -------------------------
router = DefaultRouter()
router.register(r"movies", MovieViewSet)
router.register(r"seats", SeatViewSet)
router.register(r"bookings", BookingViewSet)


# -------------------------
# URL PATTERNS
# -------------------------
urlpatterns = [
    # -------------------------
    # Template Pages (UI)
    # -------------------------
    path("", views.movie_list_page, name="movie_list"),
    path("movies/<int:movie_id>/book/", views.seat_booking_page, name="book_seat"),
    path("history/", views.booking_history_page, name="booking_history"),

    # -------------------------
    # Authentication (Login/Logout/Signup)
    # -------------------------
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("accounts/signup/", views.signup, name="signup"),

    # (Optional) If you want Django’s default auth routes too:
    # path("accounts/", include("django.contrib.auth.urls")),

    # -------------------------
    # REST API
    # -------------------------
    path("api/", include(router.urls)),
]