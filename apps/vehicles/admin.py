from django.contrib import admin
from .models import Category, Vehicle


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'price_per_day', 'fuel_type', 'transmission', 'location', 'is_available', 'is_featured')
    list_filter = ('category', 'fuel_type', 'transmission', 'is_available', 'is_featured', 'location')
    search_fields = ('name', 'brand', 'location', 'features')
    list_editable = ('price_per_day', 'is_available', 'is_featured')
