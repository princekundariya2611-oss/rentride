from rest_framework import serializers
from .models import Vehicle, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon', 'description']


class VehicleSerializer(serializers.ModelSerializer):
    category_detail = CategorySerializer(source='category', read_only=True)
    vehicle_type_display = serializers.CharField(source='get_vehicle_type_display', read_only=True)
    display_image = serializers.SerializerMethodField()

    class Meta:
        model = Vehicle
        fields = [
            'id',
            'name',
            'brand',
            'vehicle_type',
            'vehicle_type_display',
            'category',
            'category_detail',
            'price_per_day',
            'price_per_hour',
            'fuel_type',
            'transmission',
            'seats',
            'mileage',
            'year',
            'location',
            'image',
            'display_image',
            'is_available',
            'is_featured',
            'rating',
            'review_count',
            'features',
            'created_at',
        ]

    def get_display_image(self, obj):
        request = self.context.get('request')
        img_url = obj.get_display_image()
        if request and img_url and not img_url.startswith('http'):
            return request.build_absolute_uri(img_url)
        return img_url
