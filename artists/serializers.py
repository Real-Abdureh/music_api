from rest_framework import serializers
from .models import ArtistProfile, Genre

class GenreSerializer(serializers.ModelSerializer):
    """Serializer for music genres"""
    class Meta:
        model = Genre
        fields = ['id', 'name']

class ArtistProfileSerializer(serializers.ModelSerializer):
    """Serializer for artist profile"""
    user = serializers.StringRelatedField(read_only=True)  # Show username instead of ID
    genres = GenreSerializer(many=True, read_only=True)
    genre_ids = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(), source='genres', many=True, write_only=True
    )

    class Meta:
        model = ArtistProfile
        fields = ['id', 'user', 'bio', 'genres', 'genre_ids', 'availability', 'price_per_hour', 'profile_image']

    def create(self, validated_data):
        request_user = self.context['request'].user

        # Ensure only users with role "artist" can create a profile
        if request_user.role != 'artist':
            raise serializers.ValidationError("Only artists can create profiles.")

        # Check if the artist already has a profile
        if ArtistProfile.objects.filter(user=request_user).exists():
            raise serializers.ValidationError("You already have an artist profile.")

        # Extract genres before creating the profile
        genres = validated_data.pop('genres', [])
        artist_profile = ArtistProfile.objects.create(user=request_user, **validated_data)

        # Add genres if provided
        artist_profile.genres.set(genres)

        return artist_profile
