from rest_framework import generics, filters, permissions
from django.db.models import Q
from .models import Vehicle, Category
from .serializers import VehicleSerializer, CategorySerializer


class CategoryListAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class VehicleListAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = VehicleSerializer

    def get_queryset(self):
        queryset = Vehicle.objects.select_related('category').all().order_by('-created_at')
        
        vehicle_type = self.request.query_params.get('type')
        category_id = self.request.query_params.get('category')
        is_available = self.request.query_params.get('is_available')
        query = self.request.query_params.get('q')

        if vehicle_type:
            queryset = queryset.filter(vehicle_type__iexact=vehicle_type)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if is_available is not None:
            if is_available.lower() in ['true', '1']:
                queryset = queryset.filter(is_available=True)
            elif is_available.lower() in ['false', '0']:
                queryset = queryset.filter(is_available=False)
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(brand__icontains=query) |
                Q(location__icontains=query) |
                Q(category__name__icontains=query)
            )

        return queryset


class VehicleDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
