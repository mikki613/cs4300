from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Booking, Movie, Seat
from .serializers import BookingSerializer, MovieSerializer, SeatSerializer


# ----------------------------
# DRF API ViewSets
# ----------------------------

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all().order_by("title")
    serializer_class = MovieSerializer


class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all().order_by("seat_number")
    serializer_class = SeatSerializer


class BookingViewSet(viewsets.ModelViewSet):
    # ✅ REQUIRED so DRF router can determine basename automatically
    queryset = Booking.objects.all().order_by("-booking_date")
    serializer_class = BookingSerializer

    def get_queryset(self):
        # Only show bookings for the logged-in user
        if self.request.user.is_authenticated:
            return Booking.objects.filter(user=self.request.user).order_by("-booking_date")
        return Booking.objects.none()

    def create(self, request, *args, **kwargs):
        """
        POST /api/bookings/
        Body: { "movie": <movie_id>, "seat": <seat_id> }

        Books a seat for a specific movie.
        Availability is based on Booking(movie, seat) existing.
        """
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        movie_id = request.data.get("movie")
        seat_id = request.data.get("seat")

        if not movie_id or not seat_id:
            return Response({"detail": "movie and seat are required."}, status=status.HTTP_400_BAD_REQUEST)

        movie = get_object_or_404(Movie, id=movie_id)
        seat = get_object_or_404(Seat, id=seat_id)

        with transaction.atomic():
            already_booked = Booking.objects.select_for_update().filter(movie=movie, seat=seat).exists()
            if already_booked:
                return Response(
                    {"detail": "Seat already booked for this movie."},
                    status=status.HTTP_409_CONFLICT
                )

            booking = Booking.objects.create(
                movie=movie,
                seat=seat,
                user=request.user,
                booking_date=timezone.now(),
            )

        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)


# ----------------------------
# Template (HTML) Views
# ----------------------------

def movie_list_page(request):
    movies = Movie.objects.all().order_by("title")
    return render(request, "bookings/movie_list.html", {"movies": movies})


def seat_booking_page(request, movie_id):
    """
    Shows ONLY available seats for this movie.
    A seat is 'booked' for this movie if a Booking exists with (movie, seat).
    """
    movie = get_object_or_404(Movie, id=movie_id)

    booked_ids = Booking.objects.filter(movie=movie).values_list("seat_id", flat=True)
    available_seats = Seat.objects.exclude(id__in=booked_ids).order_by("seat_number")

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")

        seat_id = request.POST.get("seat_id")
        if not seat_id:
            return render(
                request,
                "bookings/seat_booking.html",
                {"movie": movie, "seats": available_seats, "error": "Please select a seat."},
            )

        seat = get_object_or_404(Seat, id=seat_id)

        with transaction.atomic():
            already_booked = Booking.objects.select_for_update().filter(movie=movie, seat=seat).exists()
            if already_booked:
                # refresh available list
                booked_ids = Booking.objects.filter(movie=movie).values_list("seat_id", flat=True)
                available_seats = Seat.objects.exclude(id__in=booked_ids).order_by("seat_number")

                return render(
                    request,
                    "bookings/seat_booking.html",
                    {"movie": movie, "seats": available_seats, "error": "That seat is already booked."},
                )

            Booking.objects.create(
                movie=movie,
                seat=seat,
                user=request.user,
                booking_date=timezone.now(),
            )

        return redirect("booking_history")

    return render(request, "bookings/seat_booking.html", {"movie": movie, "seats": available_seats})


@login_required
def booking_history_page(request):
    bookings = Booking.objects.filter(user=request.user).order_by("-booking_date")
    return render(request, "bookings/booking_history.html", {"bookings": bookings})