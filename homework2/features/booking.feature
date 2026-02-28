Feature: Booking seats

 # 1: Security / permissions

  Scenario: Unauthenticated users cannot access bookings endpoint
    When I request the bookings API without logging in
    Then the response status code should be 401 or 403

  # 2: Movie listings 

  Scenario: List movies successfully
    Given there is a movie titled "Inception"
    When I request the movies API
    Then the response status code should be 200
    And the response should contain "Inception"

  # 3: Seat availability 

  Scenario: View seat availability
    Given there is a seat "A1" that is available
    When I request the seats API
    Then the response status code should be 200
    And the response should contain "A1"

  # 4: Create a booking 

  Scenario: Authenticated user can book an available seat
  Given there is a movie titled "Inception"
  And there is a seat "A2" that is available
  And I am logged in
  When I book seat "A2" for movie "Inception"
  Then the response status code should be 201
  And seat "A2" should be marked as booked

  # 5: Prevent double-booking (edge case)

  Scenario: Cannot book an already booked seat
    Given there is a movie titled "Inception"
    And there is a seat "A1" that is available
    And I am logged in
    And seat "A1" is already booked
    When I book seat "A1" for movie "Inception"
    Then the response status code should be 400 or 409

  # 6: Booking history 

  Scenario: Authenticated user can view booking history
    Given there is a movie titled "Inception"
    And there is a seat "A1" that is available
    And I am logged in
    And I have booked seat "A1" for movie "Inception"
    When I request the bookings API while logged in
    Then the response status code should be 200
    And the response should contain "Inception"