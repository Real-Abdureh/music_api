from rest_framework import serializers
from .models import Event
from artists.models import ArtistProfile
from artists.serializers import ArtistProfileSerializer

class EventSerializer(serializers.ModelSerializer):
    """Serializer for event creation & updates"""
    organizer = serializers.StringRelatedField(read_only=True)
    artists = ArtistProfileSerializer(many=True, read_only=True)
    artist_ids = serializers.PrimaryKeyRelatedField(
        queryset=ArtistProfile.objects.all(), source='artists', many=True, write_only=True
    )

    class Meta:
        model = Event
        fields = ['id', 'organizer', 'title', 'description', 'date', 'location', 'artists', 'artist_ids']

    def create(self, validated_data):
        # Extract artist_ids before creating the event
        artist_ids = validated_data.pop('artists', [])

        # Create event (organizer is set in perform_create)
        event = Event.objects.create(**validated_data)

        # Assign artists using `.set()`
        event.artists.set(artist_ids)

        return event
