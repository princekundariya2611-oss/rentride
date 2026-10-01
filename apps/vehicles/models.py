from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    icon = models.CharField(max_length=50, default='fa-car', help_text='FontAwesome icon class e.g. fa-car, fa-motorcycle')
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    TRANSMISSION_CHOICES = (
        ('Manual', 'Manual'),
        ('Automatic', 'Automatic'),
    )

    FUEL_CHOICES = (
        ('Petrol', 'Petrol'),
        ('Diesel', 'Diesel'),
        ('Electric', 'Electric'),
        ('CNG', 'CNG'),
    )

    VEHICLE_TYPE_CHOICES = (
        ('CAR', 'Car'),
        ('BIKE', 'Bike / Scooter'),
    )

    name = models.CharField(max_length=100, help_text='e.g., Hyundai Creta, Royal Enfield Classic 350')
    brand = models.CharField(max_length=50, help_text='e.g., Hyundai, Tata, Mahindra, Honda')
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPE_CHOICES, default='CAR')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='vehicles')
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, help_text='Rental price per 24 hours in INR')
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2, default=150, help_text='Hourly rate')
    
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES, default='Petrol')
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES, default='Manual')
    seats = models.PositiveIntegerField(default=5)
    mileage = models.CharField(max_length=30, default='18 kmpl')
    year = models.PositiveIntegerField(default=2023)
    
    location = models.CharField(max_length=100, default='Morbi', help_text='Pickup location')
    image = models.ImageField(upload_to='vehicles/', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, help_text='External image URL if direct file upload is empty')
    
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.8)
    review_count = models.PositiveIntegerField(default=12)
    features = models.CharField(max_length=255, default='GPS, Bluetooth, AC, Airbags, Reverse Camera', help_text='Comma separated features')
    
    created_at = models.DateTimeField(auto_now_add=True)

    def get_display_image(self):
        if self.image:
            return self.image.url
        elif self.image_url:
            return self.image_url
        return 'https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=800&q=80'

    def __str__(self):
        return f"{self.brand} {self.name} - ₹{self.price_per_day}/day ({self.location})"
