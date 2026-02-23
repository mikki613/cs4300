from behave import when, then

@when("I request the bookings API without logging in")
def step_request_bookings(context):
    # Import AFTER Django is configured (environment.py runs before steps execute)
    from rest_framework.test import APIClient

    context.client = APIClient()
    context.response = context.client.get("/api/bookings/")

@then("the response status code should be {code:d}")
def step_check_status(context, code):
    assert context.response.status_code == code, (
        f"Expected {code}, got {context.response.status_code}"
    )