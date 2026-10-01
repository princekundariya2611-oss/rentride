from rest_framework import serializers
from .models import Booking
from apps.vehicles.serializers import VehicleSerializer


class BookingMinimalVehicleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    brand = serializers.CharField(read_only=True)
    vehicle_type_display = serializers.CharField(source='get_vehicle_type_display', read_only=True)
    price_per_day = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    image_url = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        request = self.context.get('request')
        img_url = obj.get_display_image()
        if request and img_url and not img_url.startswith('http'):
            return request.build_absolute_uri(img_url)
        return img_url


class BookingSerializer(serializers.ModelSerializer):
    vehicle_detail = BookingMinimalVehicleSerializer(source='vehicle', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id',
            'user',
            'vehicle',
            'vehicle_detail',
            'customer_name',
            'customer_phone',
            'pickup_location',
            'start_date',
            'end_date',
            'total_days',
            'total_price',
            'status',
            'status_display',
            'notes',
            'created_at',
        ]
        read_only_fields = ['total_days', 'total_price', 'created_at']

    def validate(self, attrs):
        # Trigger model clean validation logic if needed
        instance = Booking(**attrs)
        try:
            instance.clean()
        except Exception as e:
            if hasattr(e, 'message_dict'):
                raise serializers.ValidationError(e.message_dict)
            raise serializers.ValidationError(str(e))
        return attrs


class BookingStatusUpdateSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Booking
        fields = ['status', 'status_display']

    def validate_status(self, value):
        valid_statuses = [choice[0] for choice in Booking.STATUS_CHOICES]
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Invalid status '{value}'. Must be one of: {valid_statuses}")
        return value
