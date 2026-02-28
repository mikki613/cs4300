"""
Behave step definitions for the Booking Seats feature.

This file maps the Gherkin steps in booking.feature to Python code.
It uses Django models directly for setup and DRF's APIClient for API calls.
"""

from behave import given, when, then


# -------------------------
# Helper functions
# -------------------------

def _set_seat_status(seat, available: bool):
    """
    Helper to set seat availability.

    This project uses Seat.is_booked, but I added a fallback for other
    possible implementations (like booking_status) just in case.
    """
    if hasattr(seat, "is_booked"):
        seat.is_booked = (not available)
    else:
        val = getattr(seat, "booking_status", None)
        if isinstance(val, bool):
            seat.booking_status = (not available)
        else:
            seat.booking_status = "available" if available else "booked"

    seat.save()


def _response_text(response) -> str:
    """
    Safely decode an HTTP response body for debugging assert failures.
    """
    try:
        return response.content.decode("utf-8")
    except Exception:
        return str(response)


# -------------------------
# GIVEN steps
# -------------------------

@given('there is a movie titled "{title}"')
def step_given_movie(context, title):
    """
    Ensure a movie exists in the database.
    """
    from bookings.models import Movie
    from datetime import date

    context.movie, _ = Movie.objects.get_or_create(
        title=title,
        defaults={
            "description": "Test description",
            "release_date": date.today(),
            "duration": 120,
        },
    )


@given('there is a seat "{seat_number}" that is available')
def step_given_seat_available(context, seat_number):
    """
    Ensure a seat exists and is marked available.
    Also deletes any old booking for the seat from previous runs.
    """
    from bookings.models import Seat, Booking

    context.seat, _ = Seat.objects.get_or_create(seat_number=seat_number)

    # Clean up old bookings so tests don't break on reruns
    Booking.objects.filter(seat=context.seat).delete()

    _set_seat_status(context.seat, available=True)


@given('seat "{seat_number}" is already booked')
def step_given_seat_booked(context, seat_number):
    """
    Mark the seat as booked before running a booking attempt.
    """
    from bookings.models import Seat

    seat = Seat.objects.get(seat_number=seat_number)
    _set_seat_status(seat, available=False)


@given("I am logged in")
def step_given_logged_in(context):
    """
    Create (or reuse) a test user and authenticate using DRF APIClient.
    force_authenticate makes login easy for Behave tests.
    """
    from django.contrib.auth.models import User
    from rest_framework.test import APIClient

    context.user, _ = User.objects.get_or_create(username="behave_user")
    context.client = APIClient()
    context.client.force_authenticate(user=context.user)


@given('I have booked seat "{seat_number}" for movie "{title}"')
def step_given_existing_booking(context, seat_number, title):
    """
    Create an existing booking directly in the database.
    This is used for the booking history scenario.
    """
    from bookings.models import Movie, Seat, Booking
    from datetime import date

    movie = Movie.objects.get(title=title)
    seat = Seat.objects.get(seat_number=seat_number)

    _set_seat_status(seat, available=False)

    Booking.objects.get_or_create(
        movie=movie,
        seat=seat,
        user=context.user,
        defaults={"booking_date": date.today()},
    )


# -------------------------
# WHEN steps
# -------------------------

@when("I request the bookings API without logging in")
def step_when_bookings_no_auth(context):
    """Call the bookings endpoint without authentication."""
    from rest_framework.test import APIClient

    context.client = APIClient()
    context.response = context.client.get("/api/bookings/")


@when("I request the bookings API while logged in")
def step_when_bookings_auth(context):
    """Call the bookings endpoint while authenticated."""
    context.response = context.client.get("/api/bookings/")


@when("I request the movies API")
def step_when_movies(context):
    """Call the movies endpoint."""
    from rest_framework.test import APIClient

    context.client = getattr(context, "client", APIClient())
    context.response = context.client.get("/api/movies/")


@when("I request the seats API")
def step_when_seats(context):
    """Call the seats endpoint."""
    from rest_framework.test import APIClient

    context.client = getattr(context, "client", APIClient())
    context.response = context.client.get("/api/seats/")


@when('I book seat "{seat_number}" for movie "{title}"')
def step_when_book_seat(context, seat_number, title):
    """
    Attempt to create a booking using POST /api/bookings/.

    This sends IDs for movie and seat (the usual DRF pattern).
    """
    from bookings.models import Movie, Seat
    from datetime import date

    movie = Movie.objects.get(title=title)
    seat = Seat.objects.get(seat_number=seat_number)

    payload = {
        "movie": movie.id,
        "seat": seat.id,
        "user": context.user.id,
        "booking_date": str(date.today()),
    }

    context.response = context.client.post("/api/bookings/", payload, format="json")


# -------------------------
# THEN steps
# -------------------------

@then("the response status code should be {code:d}")
def step_then_status(context, code):
    """Assert a specific HTTP status code."""
    assert context.response.status_code == code, (
        f"Expected {code}, got {context.response.status_code}. "
        f"Body: {_response_text(context.response)}"
    )


@then("the response status code should be {code1:d} or {code2:d}")
def step_then_status_either(context, code1, code2):
    """Assert the response matches either of two status codes."""
    assert context.response.status_code in (code1, code2), (
        f"Expected {code1} or {code2}, got {context.response.status_code}. "
        f"Body: {_response_text(context.response)}"
    )


@then('the response should contain "{text}"')
def step_then_contains(context, text):
    """Assert the response body contains some text."""
    body = _response_text(context.response)
    assert text in body, f'Expected to find "{text}" in response. Body: {body}'


@then('seat "{seat_number}" should be marked as booked')
def step_then_seat_booked(context, seat_number):
    """
    Confirm a booking exists for the given seat.
    This is a reliable way to check "booked" even if the seat status field changes.
    """
    from bookings.models import Seat, Booking

    seat = Seat.objects.get(seat_number=seat_number)

    assert Booking.objects.filter(seat=seat).exists(), (
        f"Expected a booking to exist for seat {seat_number}, but none was found."
    )