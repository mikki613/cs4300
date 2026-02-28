from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views
from .views import BookingViewSet, MovieViewSet, SeatViewSet

router = DefaultRouter()
router.register(r"movies", MovieViewSet)
router.register(r"seats", SeatViewSet)
router.register(r"bookings", BookingViewSet)

urlpatterns = [
    # Template routes
    path("", views.movie_list_page, name="movie_list"),
    path("movies/<int:movie_id>/book/", views.seat_booking_page, name="book_seat"),
    path("history/", views.booking_history_page, name="booking_history"),

    # API routes
    path("api/", include(router.urls)),
]