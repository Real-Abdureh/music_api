from django.urls import path
from .views import BookingCreateView, BookingDetailView, BookingListView

urlpatterns = [
    path('create/', BookingCreateView.as_view(), name='booking-create'),
    path('<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),
    path('list/', BookingListView.as_view(), name='booking-list'),
]
