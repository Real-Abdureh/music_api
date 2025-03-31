from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from events.models import Event

User = get_user_model()


class EventAPITestCase(APITestCase):
    

    def setUp(self):
        
        # Create test users
        self.organizer = User.objects.create_user(username="event_organizer", password="testpass", role="organizer")
        self.attendee = User.objects.create_user(username="attendee_user", password="testpass", role="attendee")

        # Generate JWT tokens
        self.organizer_token = str(RefreshToken.for_user(self.organizer).access_token)
        self.attendee_token = str(RefreshToken.for_user(self.attendee).access_token)

        # Create an event
        self.event = Event.objects.create(
            organizer=self.organizer,
            title="Summer Music Festival",
            description="A great event for music lovers.",
            date="2025-06-20T19:00:00Z",
            location="Los Angeles"
        )

    def authenticate_as_organizer(self):

        self.client.force_authenticate(user=self.organizer)

    def authenticate_as_attendee(self):
        
        self.client.force_authenticate(user=self.attendee)

    def test_create_event(self):
        
        self.authenticate_as_organizer()
        data = {
            "title": "New Music Fest",
            "description": "A fun event",
            "date": "2025-07-10T18:00:00Z",
            "location": "New York",
            "artist_ids": [] 
        }
        response = self.client.post("/api/events/create/", data, format="json")
        print("Create Event Response:", response.data) 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_event_unauthorized(self):
        """Test that an attendee (non-organizer) cannot create an event"""
        self.authenticate_as_attendee()
        data = {
            "title": "Unauthorized Fest",
            "description": "Should not be allowed",
            "date": "2025-08-15T18:00:00Z",
            "location": "Chicago",
            "artist_ids": [] 
        }
        response = self.client.post("/api/events/create/", data, format="json")
        print("Unauthorized Create Event Response:", response.data)  
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  

    def test_get_event_details(self):
        
        self.authenticate_as_organizer()
        response = self.client.get(f"/api/events/{self.event.id}/")
        print("Event Details Response:", response.data)  
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_events(self):
        
        self.authenticate_as_organizer()
        response = self.client.get("/api/events/list/")
        print("List Events Response:", response.data) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_event(self):
       
        self.authenticate_as_organizer()
        data = {"title": "Updated Summer Festival"}
        response = self.client.patch(f"/api/events/{self.event.id}/", data, format="json")
        print("Update Event Response:", response.data)  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.event.refresh_from_db()
        self.assertEqual(self.event.title, "Updated Summer Festival")

    def test_update_event_unauthorized(self):
        
        self.authenticate_as_attendee()
        data = {"title": "Hacked Festival"}

        
        response = self.client.patch(f"/api/events/{self.event.id}/", data, format="json")

        print("Unauthorized Update Event Response:", response.data)  
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  

    def test_delete_event(self):
        
        self.authenticate_as_organizer()
        response = self.client.delete(f"/api/events/{self.event.id}/")
        print("Delete Event Response:", response.status_code)  
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Event.objects.filter(id=self.event.id).exists())

    def test_delete_event_unauthorized(self):
        
        self.authenticate_as_attendee()

        
        event_exists = Event.objects.filter(id=self.event.id).exists()
        self.assertTrue(event_exists, "Event should exist before attempting deletion")

        response = self.client.delete(f"/api/events/{self.event.id}/")
        print("Unauthorized Delete Event Response:", response.status_code)  
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  

