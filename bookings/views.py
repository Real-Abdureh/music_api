from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Booking
from .serializers import BookingSerializer

class BookingCreateView(generics.CreateAPIView):
    """API view to create a new booking"""
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != "organizer":
            raise PermissionDenied("Only organizers can create bookings.")
        serializer.save(organizer=self.request.user)  # Set organizer here


class BookingDetailView(generics.RetrieveUpdateAPIView):
    """API view to retrieve or update a booking"""
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == "organizer":
            return Booking.objects.filter(organizer=self.request.user)
        elif self.request.user.role == "artist":
            return Booking.objects.filter(artist__user=self.request.user)
        return Booking.objects.none()

    def perform_update(self, serializer):
        booking = self.get_object()
        if self.request.user.role == "organizer" and booking.organizer != self.request.user:
            raise PermissionDenied("You can only update your own bookings.")
        if self.request.user.role == "artist" and booking.artist.user != self.request.user:
            raise PermissionDenied("You can only accept or reject your own bookings.")
        
        serializer.save()

class BookingListView(generics.ListAPIView):
    """API view to list bookings for an organizer or artist"""
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == "organizer":
            return Booking.objects.filter(organizer=self.request.user)
        elif self.request.user.role == "artist":
            return Booking.objects.filter(artist__user=self.request.user)
        return Booking.objects.none()
