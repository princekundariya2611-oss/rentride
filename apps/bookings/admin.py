from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'customer_phone', 'vehicle', 'start_date', 'end_date', 'total_days', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'start_date', 'pickup_location')
    search_fields = ('customer_name', 'customer_phone', 'vehicle__name', 'vehicle__brand')
    list_editable = ('status',)
