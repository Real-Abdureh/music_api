from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import ArtistProfile, Genre
from .serializers import ArtistProfileSerializer, GenreSerializer

class GenreListView(generics.ListCreateAPIView):
    """API view to list or create music genres"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticated]




class CreateArtistProfileView(generics.CreateAPIView):
    """API view to create an artist profile for the authenticated user."""
    serializer_class = ArtistProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()
 


class ArtistProfileView(generics.RetrieveUpdateAPIView):
    """API view for an artist to manage their profile"""
    serializer_class = ArtistProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        if not hasattr(self.request.user, 'artist_profile'):
            raise PermissionDenied("You don't have an artist profile.")
        return self.request.user.artist_profile

class ArtistListView(generics.ListAPIView):
    """API view to list all artists"""
    queryset = ArtistProfile.objects.all()
    serializer_class = ArtistProfileSerializer
    permission_classes = [permissions.AllowAny]
