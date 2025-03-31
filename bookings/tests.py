from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from artists.models import ArtistProfile
from events.models import Event
from bookings.models import Booking

User = get_user_model()

class BookingAPITestCase(APITestCase):
   

    def setUp(self):
        
        # Create test users
        self.organizer = User.objects.create_user(
            username="event_organizer", password="testpass", role="organizer"
        )
        self.artist_user = User.objects.create_user(
            username="john_doe", password="testpass", role="artist"
        )

        # Create an artist profile
        self.artist_profile = ArtistProfile.objects.create(
            user=self.artist_user, bio="Hip-Hop artist", price_per_hour=100
        )

        # Create an event
        self.event = Event.objects.create(
            organizer=self.organizer,
            title="Summer Music Festival",
            description="A great event for music lovers.",
            date="2025-06-20T19:00:00Z",
            location="Los Angeles",
        )

        # Create a booking
        self.booking = Booking.objects.create(
            organizer=self.organizer,
            artist=self.artist_profile,
            event=self.event,
            hours_booked=3,
        )

        # Authenticate as organizer
        self.organizer_token = self.get_access_token(self.organizer)
        self.artist_token = self.get_access_token(self.artist_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.organizer_token}")

    def get_access_token(self, user):
        
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_create_booking(self):
       
        data = {
            "artist_id": self.artist_profile.id,
            "event_id": self.event.id,
            "hours_booked": 2,
        }
        response = self.client.post("/api/bookings/create/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["organizer"], self.organizer.username)
        self.assertEqual(response.data["total_price"], 200.00)

    def test_create_booking_invalid_role(self):
       
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.artist_token}")  # Authenticate as artist
        data = {
            "artist_id": self.artist_profile.id,
            "event_id": self.event.id,
            "hours_booked": 2,
        }
        response = self.client.post("/api/bookings/create/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Forbidden

    def test_get_booking_details(self):
        
        response = self.client.get(f"/api/bookings/{self.booking.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.booking.id)
        self.assertEqual(response.data["status"], "pending")

    def test_update_booking_status(self):
        
        data = {"status": "confirmed"}
        response = self.client.patch(f"/api/bookings/{self.booking.id}/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)  # Include response data for debugging
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, "confirmed")


    def test_list_bookings(self):

        response = self.client.get("/api/bookings/list/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_delete_booking(self):
        
        response = self.client.delete(f"/api/bookings/{self.booking.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Booking.objects.filter(id=self.booking.id).exists())

