from behave import given, when, then



def _set_seat_status(seat, available: bool):
    """
    Supports:
    - Seat.is_booked (BooleanField) 
    - Seat.booking_status (legacy/other versions)
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
    try:
        return response.content.decode("utf-8")
    except Exception:
        return str(response)



@given('there is a movie titled "{title}"')
def step_given_movie(context, title):
    # Import AFTER django is configured (environment.py runs before steps)
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
    from bookings.models import Seat, Booking

    context.seat, _ = Seat.objects.get_or_create(seat_number=seat_number)

    # IMPORTANT: Clean up any old booking for this seat from previous test runs
    Booking.objects.filter(seat=context.seat).delete()

    _set_seat_status(context.seat, available=True)


@given('seat "{seat_number}" is already booked')
def step_given_seat_booked(context, seat_number):
    from bookings.models import Seat

    seat = Seat.objects.get(seat_number=seat_number)
    _set_seat_status(seat, available=False)


@given("I am logged in")
def step_given_logged_in(context):
    """
    Uses DRF's APIClient.force_authenticate so you don't need to implement login endpoints.
    """
    from django.contrib.auth.models import User
    from rest_framework.test import APIClient

    context.user, _ = User.objects.get_or_create(username="behave_user")
    context.client = APIClient()
    context.client.force_authenticate(user=context.user)


@given('I have booked seat "{seat_number}" for movie "{title}"')
def step_given_existing_booking(context, seat_number, title):
    """
    Creates an existing booking directly via the database.
    This avoids depending on the API create endpoint for the history scenario.
    """
    from bookings.models import Movie, Seat, Booking
    from datetime import date

    movie = Movie.objects.get(title=title)
    seat = Seat.objects.get(seat_number=seat_number)

    # mark booked
    _set_seat_status(seat, available=False)

    # create booking row
    Booking.objects.get_or_create(
        movie=movie,
        seat=seat,
        user=context.user,
        defaults={"booking_date": date.today()},
    )



@when("I request the bookings API without logging in")
def step_when_bookings_no_auth(context):
    from rest_framework.test import APIClient

    context.client = APIClient()
    context.response = context.client.get("/api/bookings/")


@when("I request the bookings API while logged in")
def step_when_bookings_auth(context):
    # context.client already authenticated in "I am logged in"
    context.response = context.client.get("/api/bookings/")


@when("I request the movies API")
def step_when_movies(context):
    from rest_framework.test import APIClient

    context.client = getattr(context, "client", APIClient())
    context.response = context.client.get("/api/movies/")


@when("I request the seats API")
def step_when_seats(context):
    from rest_framework.test import APIClient

    context.client = getattr(context, "client", APIClient())
    context.response = context.client.get("/api/seats/")


@when('I book seat "{seat_number}" for movie "{title}"')
def step_when_book_seat(context, seat_number, title):
    """
    Posts to /api/bookings/ using ids.
    Assumes your Booking serializer accepts: movie, seat, user, booking_date (typical).
    If your API uses a custom booking endpoint, tell me the URL and I’ll adjust this.
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


@then("the response status code should be {code:d}")
def step_then_status(context, code):
    assert context.response.status_code == code, (
        f"Expected {code}, got {context.response.status_code}. "
        f"Body: {_response_text(context.response)}"
    )


@then("the response status code should be {code1:d} or {code2:d}")
def step_then_status_either(context, code1, code2):
    assert context.response.status_code in (code1, code2), (
        f"Expected {code1} or {code2}, got {context.response.status_code}. "
        f"Body: {_response_text(context.response)}"
    )


@then('the response should contain "{text}"')
def step_then_contains(context, text):
    body = _response_text(context.response)
    assert text in body, f'Expected to find "{text}" in response. Body: {body}'


@then('seat "{seat_number}" should be marked as booked')
def step_then_seat_booked(context, seat_number):
    from bookings.models import Seat, Booking

    seat = Seat.objects.get(seat_number=seat_number)

    assert Booking.objects.filter(seat=seat).exists(), (
        f"Expected a booking to exist for seat {seat_number}, but none was found."
    )