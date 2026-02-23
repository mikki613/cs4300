from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Movie, Seat, Booking
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer


# -------------------------
# API VIEWSETS
# -------------------------

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all().order_by("release_date")
    serializer_class = MovieSerializer
    permission_classes = [permissions.AllowAny]


class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all().order_by("seat_number")
    serializer_class = SeatSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def book(self, request, pk=None):
        """
        POST /api/seats/<id>/book/
        Body: {"movie": <movie_id>}
        """
        seat = self.get_object()
        if seat.is_booked:
            return Response({"detail": "Seat is already booked."}, status=status.HTTP_400_BAD_REQUEST)

        movie_id = request.data.get("movie")
        if not movie_id:
            return Response({"detail": "movie is required."}, status=status.HTTP_400_BAD_REQUEST)

        movie = get_object_or_404(Movie, pk=movie_id)

        booking = Booking.objects.create(movie=movie, seat=seat, user=request.user)
        seat.is_booked = True
        seat.save()

        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all().order_by("-booking_date")
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only show the current user's bookings (booking history)
        return Booking.objects.filter(user=self.request.user).order_by("-booking_date")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# -------------------------
# TEMPLATE (UI) VIEWS
# -------------------------

def movie_list_page(request):
    movies = Movie.objects.all().order_by("release_date")
    return render(request, "bookings/movie_list.html", {"movies": movies})


@login_required
def seat_booking_page(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    seats = Seat.objects.all().order_by("seat_number")

    if request.method == "POST":
        seat_id = request.POST.get("seat_id")
        seat = get_object_or_404(Seat, pk=seat_id)

        if seat.is_booked:
            messages.error(request, "That seat is already booked.")
            return redirect("book_seat", movie_id=movie.id)

        Booking.objects.create(movie=movie, seat=seat, user=request.user)
        seat.is_booked = True
        seat.save()

        messages.success(request, f"Booked seat {seat.seat_number} for {movie.title}!")
        return redirect("booking_history")

    return render(request, "bookings/seat_booking.html", {"movie": movie, "seats": seats})


@login_required
def booking_history_page(request):
    bookings = Booking.objects.filter(user=request.user).order_by("-booking_date")
    return render(request, "bookings/booking_history.html", {"bookings": bookings})