from django.db import models
from django.conf import settings
from artists.models import ArtistProfile
from events.models import Event

class Booking(models.Model):
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    artist = models.ForeignKey(ArtistProfile, on_delete=models.CASCADE, related_name="bookings")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="bookings")
    hours_booked = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("confirmed", "Confirmed"), ("cancelled", "Cancelled")],
        default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_price = self.hours_booked * self.artist.price_per_hour
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.organizer.username} booked {self.artist.user.username} for {self.event.title}"
