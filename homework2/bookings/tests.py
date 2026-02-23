from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from .models import Movie, Seat, Booking


class MovieSeatBookingAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="pass1234")
        self.other_user = User.objects.create_user(username="otheruser", password="pass1234")

        self.movie = Movie.objects.create(
            title="Test Movie",
            description="Test description",
            release_date="2024-01-01",
            duration=120,
        )

        self.seat = Seat.objects.create(seat_number="T1", is_booked=False)
        self.seat2 = Seat.objects.create(seat_number="T2", is_booked=False)

    # -------- Movies API --------
    def test_movies_list_returns_200(self):
        resp = self.client.get("/api/movies/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(len(resp.data) >= 1)

    def test_movies_create_returns_201(self):
        payload = {
            "title": "New Movie",
            "description": "Desc",
            "release_date": "2025-01-01",
            "duration": 100,
        }
        resp = self.client.post("/api/movies/", payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    # -------- Seats API --------
    def test_seats_list_returns_200(self):
        resp = self.client.get("/api/seats/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    # -------- Booking action --------
    def test_book_seat_requires_auth(self):
        resp = self.client.post(
            f"/api/seats/{self.seat.id}/book/",
            {"movie": self.movie.id},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_book_seat_success(self):
        self.client.login(username="testuser", password="pass1234")

        resp = self.client.post(
            f"/api/seats/{self.seat.id}/book/",
            {"movie": self.movie.id},
            format="json",
        )

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        self.seat.refresh_from_db()
        self.assertTrue(self.seat.is_booked)
        self.assertEqual(Booking.objects.filter(user=self.user).count(), 1)

    def test_book_already_booked_seat_fails(self):
        self.client.login(username="testuser", password="pass1234")

        # first booking
        self.client.post(
            f"/api/seats/{self.seat.id}/book/",
            {"movie": self.movie.id},
            format="json",
        )

        # second booking attempt
        resp2 = self.client.post(
            f"/api/seats/{self.seat.id}/book/",
            {"movie": self.movie.id},
            format="json",
        )

        self.assertEqual(resp2.status_code, status.HTTP_400_BAD_REQUEST)

    # -------- Booking history API --------
    def test_booking_history_only_shows_logged_in_user(self):
        # Create booking for other user
        Booking.objects.create(movie=self.movie, seat=self.seat2, user=self.other_user)
        self.seat2.is_booked = True
        self.seat2.save()

        self.client.login(username="testuser", password="pass1234")
        resp = self.client.get("/api/bookings/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 0)