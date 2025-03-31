from django.urls import path
from .views import ArtistProfileView, ArtistListView, GenreListView, CreateArtistProfileView

urlpatterns = [
    path('genres/', GenreListView.as_view(), name='genre-list'),
    path("create/", CreateArtistProfileView.as_view(), name="create-artist-profile"),
    path('profile/', ArtistProfileView.as_view(), name='artist-profile'),
    path('list/', ArtistListView.as_view(), name='artist-list'),
]
