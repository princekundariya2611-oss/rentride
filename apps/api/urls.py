from django.urls import path
from apps.vehicles import api_views as vehicle_api
from apps.bookings import api_views as booking_api

app_name = 'api'

urlpatterns = [
    # Vehicles API
    path('vehicles/', vehicle_api.VehicleListAPIView.as_view(), name='vehicle-list'),
    path('vehicles/<int:pk>/', vehicle_api.VehicleDetailAPIView.as_view(), name='vehicle-detail'),
    path('categories/', vehicle_api.CategoryListAPIView.as_view(), name='category-list'),

    # Bookings API
    path('bookings/', booking_api.BookingListCreateAPIView.as_view(), name='booking-list-create'),
    path('bookings/<int:pk>/', booking_api.BookingDetailAPIView.as_view(), name='booking-detail'),
    path('bookings/<int:pk>/status/', booking_api.BookingStatusUpdateAPIView.as_view(), name='booking-status-update'),
    path('bookings/stats/', booking_api.BookingStatsAPIView.as_view(), name='booking-stats'),
]
