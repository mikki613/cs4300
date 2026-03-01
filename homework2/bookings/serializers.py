"""
Serializers for the Movie Theater Booking application.

These serializers convert model instances into JSON format
and validate incoming data for API requests.
"""

from rest_framework import serializers
from .models import Movie, Seat, Booking


class MovieSerializer(serializers.ModelSerializer):

    """
    Serializer for the Movie model.

    Converts Movie objects to and from JSON representation.
    """

    class Meta:
        model = Movie
        fields = "__all__"


class SeatSerializer(serializers.ModelSerializer):

    """
    Serializer for the Seat model.

    Used to represent seat data in API responses.
    """

    class Meta:
        model = Seat
        fields = "__all__"


class BookingSerializer(serializers.ModelSerializer):

    """
    Serializer for the Booking model.

    Handles validation and serialization of booking data,
    including movie, seat, and user relationships.
    """
    class Meta:
        model = Booking
        fields = "__all__"