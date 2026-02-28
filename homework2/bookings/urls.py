from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views
from . import views

from .views import MovieViewSet, SeatViewSet, BookingViewSet

router = DefaultRouter()
router.register(r"movies", MovieViewSet)
router.register(r"seats", SeatViewSet)
router.register(r"bookings", BookingViewSet)

urlpatterns = [
    # UI pages
    path("", views.movie_list_page, name="movie_list"),
    path("movies/<int:movie_id>/book/", views.seat_booking_page, name="book_seat"),
    path("history/", views.booking_history_page, name="booking_history"),

    # Auth pages
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("accounts/signup/", views.signup, name="signup"),

    # Django built-in auth extras (password reset/change etc.)
    path("accounts/", include("django.contrib.auth.urls")),

    # API
    path("api/", include(router.urls)),
]