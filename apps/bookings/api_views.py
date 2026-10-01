from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404

from .models import Booking
from .serializers import (
    BookingSerializer,
    BookingStatusUpdateSerializer
)


class BookingListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = BookingSerializer

    def get_queryset(self):
        queryset = Booking.objects.select_related('vehicle', 'user').all().order_by('-created_at')
        
        status_param = self.request.query_params.get('status')
        query = self.request.query_params.get('q')

        if status_param and status_param.upper() != 'ALL':
            queryset = queryset.filter(status=status_param.upper())

        if query:
            query = query.strip()
            queryset = queryset.filter(
                Q(customer_name__icontains=query) |
                Q(customer_phone__icontains=query) |
                Q(vehicle__name__icontains=query) |
                Q(vehicle__brand__icontains=query) |
                Q(pickup_location__icontains=query)
            )

        return queryset

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(user=user)


class BookingDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class BookingStatusUpdateAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def patch(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)
        serializer = BookingStatusUpdateSerializer(booking, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            # Calculate updated stats to send back in response
            all_bookings = Booking.objects.all()
            stats = {
                'total_bookings': all_bookings.count(),
                'pending_count': all_bookings.filter(status='PENDING').count(),
                'confirmed_count': all_bookings.filter(status='CONFIRMED').count(),
                'active_count': all_bookings.filter(status='ACTIVE').count(),
                'completed_count': all_bookings.filter(status='COMPLETED').count(),
                'cancelled_count': all_bookings.filter(status='CANCELLED').count(),
                'total_revenue': float(all_bookings.exclude(status='CANCELLED').aggregate(Sum('total_price'))['total_price__sum'] or 0),
            }

            return Response({
                'message': f"Booking #{booking.id} status updated to '{booking.get_status_display()}'.",
                'booking': BookingSerializer(booking, context={'request': request}).data,
                'stats': stats
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookingStatsAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        all_bookings = Booking.objects.all()
        stats = {
            'total_bookings': all_bookings.count(),
            'pending_count': all_bookings.filter(status='PENDING').count(),
            'confirmed_count': all_bookings.filter(status='CONFIRMED').count(),
            'active_count': all_bookings.filter(status='ACTIVE').count(),
            'completed_count': all_bookings.filter(status='COMPLETED').count(),
            'cancelled_count': all_bookings.filter(status='CANCELLED').count(),
            'total_revenue': float(all_bookings.exclude(status='CANCELLED').aggregate(Sum('total_price'))['total_price__sum'] or 0),
        }
        return Response(stats, status=status.HTTP_200_OK)
