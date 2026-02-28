"""
Serializers for the Movie Theater Booking application.

These serializers convert model instances (Movie, Seat, Booking)
into JSON format for the REST API and handle validation logic.
"""

from rest_framework import serializers
from .models import Movie, Seat, Booking


class MovieSerializer(serializers.ModelSerializer):
    """
    Serializer for Movie model.
    Converts movie data to/from JSON format.
    """

    class Meta:
        model = Movie
        fields = ["id", "title", "description", "release_date", "duration"]


class SeatSerializer(serializers.ModelSerializer):
    """
    Serializer for Seat model.
    Exposes seat number and booking status.
    """

    class Meta:
        model = Seat
        fields = ["id", "seat_number", "is_booked"]


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for Booking model.

    Includes extra read-only fields to display:
    - movie_title
    - seat_number

    Also contains validation logic to prevent double booking.
    """

    movie_title = serializers.CharField(source="movie.title", read_only=True)
    seat_number = serializers.CharField(source="seat.seat_number", read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id",
            "movie",
            "movie_title",
            "seat",
            "seat_number",
            "user",
            "booking_date",
        ]
        read_only_fields = ["user", "booking_date"]

    def validate_seat(self, seat):
        """
        Prevent booking a seat that is already booked.
        """

        # Block booking if seat is already marked as booked
        if getattr(seat, "is_booked", False):
            raise serializers.ValidationError("This seat is already booked.")

        # Extra safety check in case a booking already exists
        if Booking.objects.filter(seat=seat).exists():
            raise serializers.ValidationError("This seat is already booked.")

        return seat

    def create(self, validated_data):
        """
        Create a booking and automatically mark the seat as booked.
        """

        booking = Booking.objects.create(**validated_data)

        # Mark the seat as booked
        seat = booking.seat
        seat.is_booked = True
        seat.save()

        return booking