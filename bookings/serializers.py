from rest_framework import serializers
from .models import Booking



class BookingSerializer(serializers.ModelSerializer):
    """Serializer for booking transactions"""
    organizer = serializers.StringRelatedField(read_only=True)  # Display organizer username
    artist = serializers.StringRelatedField(read_only=True)  # Display artist username
    event = serializers.StringRelatedField(read_only=True)  # Display event title
    artist_id = serializers.PrimaryKeyRelatedField(
        queryset=Booking._meta.get_field('artist').related_model.objects.all(),
        source="artist",
        write_only=True
    )
    event_id = serializers.PrimaryKeyRelatedField(
        queryset=Booking._meta.get_field('event').related_model.objects.all(),
        source="event",
        write_only=True
    )

    class Meta:
        model = Booking
        fields = ["id", "organizer", "artist", "event", "artist_id", "event_id", "hours_booked", "total_price", "status", "created_at"]
        read_only_fields = ["total_price", "organizer", "status", "created_at"]

    def create(self, validated_data):
        return Booking.objects.create(**validated_data)  # Remove organizer from here