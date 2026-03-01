"""
Views for the Movie Theater Booking application.

Includes:
- DRF ViewSets (API)
- Template views (website)
- Auth views required by movie_theater_booking/urls.py (signup)
"""

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Booking, Movie, Seat
from .serializers import BookingSerializer, MovieSerializer, SeatSerializer


# =========================
# AUTH / ACCOUNTS
# =========================

def signup(request):
    """
    User signup page.
    Required because movie_theater_booking/urls.py maps:
    path("accounts/signup/", booking_views.signup, name="signup")
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("movie_list")
    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form": form})


# =========================
# DRF API VIEWSETS
# =========================

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all().order_by("id")
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all().order_by("seat_number")
    serializer_class = SeatSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all().order_by("-booking_date")
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# =========================
# TEMPLATE / WEBSITE VIEWS
# =========================

def movie_list_page(request):
    """
    Homepage showing all movies.
    bookings/urls.py expects this function name.
    """
    movies = Movie.objects.all().order_by("id")
    return render(request, "bookings/movie_list.html", {"movies": movies})


@login_required(login_url="login")
def booking_history(request):
    """
    Show the logged-in user's booking history.
    """
    bookings = (
        Booking.objects.filter(user=request.user)
        .select_related("movie", "seat")
        .order_by("-booking_date")
    )
    return render(request, "bookings/booking_history.html", {"bookings": bookings})


# Some projects wire this name in urls.py; keep as alias to avoid future crashes.
booking_history_page = booking_history


def seat_booking_page(request, movie_id):
    """
    Page to book a seat for a specific movie.
    Available seats = all seats - seats booked for this movie.
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

        try:
            with transaction.atomic():
                Booking.objects.create(
                    movie=movie,
                    seat=seat,
                    user=request.user,
                    booking_date=timezone.now(),
                )
        except IntegrityError:
            booked_ids = Booking.objects.filter(movie=movie).values_list("seat_id", flat=True)
            available_seats = Seat.objects.exclude(id__in=booked_ids).order_by("seat_number")
            return render(
                request,
                "bookings/seat_booking.html",
                {"movie": movie, "seats": available_seats, "error": "That seat was just booked. Pick another."},
            )

        return redirect("booking_history")

    return render(request, "bookings/seat_booking.html", {"movie": movie, "seats": available_seats})