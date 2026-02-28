"""
Unit and integration tests for the bookings app.

These tests mainly check that:
- The Movies and Seats API endpoints work
- Booking a seat requires authentication
- Booking a seat marks it as booked
- Double booking is prevented
- Booking history only shows the logged-in user's bookings
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from .models import Movie, Seat, Booking


class MovieSeatBookingAPITests(TestCase):
    """
    Tests for the main API functionality in this project.
    """

    def setUp(self):
        """
        Set up a test client, users, and some starter objects
        so each test can run independently.
        """
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
        """GET /api/movies/ should return 200 and at least one movie."""
        resp = self.client.get("/api/movies/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(len(resp.data) >= 1)

    def test_movies_create_returns_201(self):
        """POST /api/movies/ should create a new movie and return 201."""
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
        """GET /api/seats/ should return 200."""
        resp = self.client.get("/api/seats/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    # -------- Booking action --------
    def test_book_seat_requires_auth(self):
        """
        Booking a seat without being logged in should fail.
        Some setups return 401, others return 403, so we accept either.
        """
        resp = self.client.post(
            f"/api/seats/{self.seat.id}/book/",
            {"movie": self.movie.id},
            format="json",
        )
        self.assertIn(resp.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_book_seat_success(self):
        """Authenticated user should be able to book a seat successfully."""
        self.client.force_authenticate(user=self.user)

        resp = self.client.post(
            f"/api/seats/{self.seat.id}/book/",
            {"movie": self.movie.id},
            format="json",
        )

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # Seat should now be marked booked
        self.seat.refresh_from_db()
        self.assertTrue(self.seat.is_booked)

        # Booking should exist and match the movie/seat
        booking = Booking.objects.get(user=self.user)
        self.assertEqual(booking.movie_id, self.movie.id)
        self.assertEqual(booking.seat_id, self.seat.id)

    def test_book_already_booked_seat_fails(self):
        """Trying to book the same seat twice should fail."""
        self.client.force_authenticate(user=self.user)

        # First booking should succeed
        resp1 = self.client.post(
            f"/api/seats/{self.seat.id}/book/",
            {"movie": self.movie.id},
            format="json",
        )
        self.assertEqual(resp1.status_code, status.HTTP_201_CREATED)

        # Second booking attempt should fail
        resp2 = self.client.post(
            f"/api/seats/{self.seat.id}/book/",
            {"movie": self.movie.id},
            format="json",
        )
        self.assertIn(resp2.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_409_CONFLICT])

    # -------- Booking history API --------
    def test_booking_history_only_shows_logged_in_user(self):
        """GET /api/bookings/ should only return bookings belonging to the logged-in user."""
        # Booking for other user
        Booking.objects.create(movie=self.movie, seat=self.seat2, user=self.other_user)
        self.seat2.is_booked = True
        self.seat2.save()

        # Booking for logged-in user
        Booking.objects.create(movie=self.movie, seat=self.seat, user=self.user)
        self.seat.is_booked = True
        self.seat.save()

        self.client.force_authenticate(user=self.user)

        resp = self.client.get("/api/bookings/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # Should only see the logged-in user's booking
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]["user"], self.user.id)