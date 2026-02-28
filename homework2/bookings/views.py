from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from rest_framework import viewsets

from .models import Movie, Seat, Booking
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer


# -----------------------------
# DRF API ViewSets
# -----------------------------
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


# -----------------------------
# Auth (Signup)
# -----------------------------
def signup(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form": form})


# -----------------------------
# HTML Pages
# -----------------------------
def movie_list_page(request):
    movies = Movie.objects.all().order_by("title")
    return render(request, "bookings/movie_list.html", {"movies": movies})


@login_required
def seat_booking_page(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)

    # Seats that do NOT have a booking for THIS movie
    available_seats = Seat.objects.exclude(bookings__movie=movie).order_by("seat_number")

    if request.method == "POST":
        seat_id = request.POST.get("seat_id")
        if not seat_id:
            return render(
                request,
                "bookings/seat_booking.html",
                {
                    "movie": movie,
                    "available_seats": available_seats,
                    "error": "Please select a seat.",
                },
            )

        seat = get_object_or_404(Seat, pk=seat_id)

        try:
            Booking.objects.create(user=request.user, movie=movie, seat=seat)
        except IntegrityError:
            # Someone booked it right before this user submitted
            return render(
                request,
                "bookings/seat_booking.html",
                {
                    "movie": movie,
                    "available_seats": Seat.objects.exclude(bookings__movie=movie).order_by("seat_number"),
                    "error": "That seat was just booked. Choose another.",
                },
            )

        return redirect(reverse("booking_history"))

    return render(
        request,
        "bookings/seat_booking.html",
        {"movie": movie, "available_seats": available_seats},
    )


@login_required
def booking_history_page(request):
    bookings = Booking.objects.filter(user=request.user).select_related("movie", "seat").order_by("-booking_time")
    return render(request, "bookings/booking_history.html", {"bookings": bookings})