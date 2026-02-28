"""
URLs for the bookings app.

I put the UI pages (templates) first, then auth routes, then API routes.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views

from .views import (
    MovieViewSet,
    SeatViewSet,
    BookingViewSet,
    movie_list_page,
    seat_booking_page,
    booking_history_page,
    signup,
)

router = DefaultRouter()
router.register(r"movies", MovieViewSet)
router.register(r"seats", SeatViewSet)
router.register(r"bookings", BookingViewSet)

urlpatterns = [
    # UI pages
    path("", movie_list_page, name="movie_list"),
    path("movies/<int:movie_id>/book/", seat_booking_page, name="book_seat"),
    path("history/", booking_history_page, name="booking_history"),

    # Auth pages
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("accounts/signup/", signup, name="signup"),

    # API
    path("api/", include(router.urls)),
]