from rest_framework import serializers
from .models import Movie, Seat, Booking


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["id", "title", "description", "release_date", "duration"]


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ["id", "seat_number", "is_booked"]


class BookingSerializer(serializers.ModelSerializer):
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
        # Block booking if seat is already marked booked
        if getattr(seat, "is_booked", False):
            raise serializers.ValidationError("This seat is already booked.")

        # Also block if there is already a booking row for this seat
        if Booking.objects.filter(seat=seat).exists():
            raise serializers.ValidationError("This seat is already booked.")

        return seat

    #  Automatically set seat as booked when creating booking
    def create(self, validated_data):
        booking = Booking.objects.create(**validated_data)

        # mark seat as booked
        seat = booking.seat
        seat.is_booked = True
        seat.save()

        return booking 