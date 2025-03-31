from django.db import models
from django.conf import settings

class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class ArtistProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="artist_profile")
    bio = models.TextField()
    genres = models.ManyToManyField(Genre, blank=True)
    availability = models.BooleanField(default=True)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    profile_image = models.ImageField(upload_to="artist_profiles/", blank=True, null=True)

    def __str__(self):
        return self.user.username
