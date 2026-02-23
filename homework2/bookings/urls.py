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

router = DefaultRouter()
router.register(r"movies", MovieViewSet)
router.register(r"seats", SeatViewSet)
router.register(r"bookings", BookingViewSet)

urlpatterns = [
    # Template pages
    path("", movie_list_page, name="movie_list"),
    path("movies/<int:movie_id>/book/", seat_booking_page, name="book_seat"),
    path("history/", booking_history_page, name="booking_history"),

    # API
    path("api/", include(router.urls)),
]