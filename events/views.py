from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Event
from .serializers import EventSerializer

class EventCreateView(generics.CreateAPIView):
    """API view for organizers to create events"""
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        request_user = self.request.user  
        serializer.save(organizer=request_user) 

class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    """API view to retrieve, update, or delete an event"""
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Event.objects.filter(organizer=self.request.user)

    def perform_update(self, serializer):
        event = self.get_object()
        if event.organizer != self.request.user:
            raise PermissionDenied("You can only edit your own events.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.organizer != self.request.user:
            raise PermissionDenied("You can only delete your own events.")
        instance.delete()

class EventListView(generics.ListAPIView):
    """API view to list all events (public)"""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]
