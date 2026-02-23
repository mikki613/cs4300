Feature: Booking seats

  Scenario: Unauthenticated users cannot access bookings endpoint
    When I request the bookings API without logging in
    Then the response status code should be 403