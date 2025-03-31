from django.db import models
from django.conf import settings
from artists.models import ArtistProfile

class Event(models.Model):
    """Model for events created by organizers"""
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    artists = models.ManyToManyField(ArtistProfile, related_name="events", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
