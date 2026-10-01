from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = 'CUSTOMER', 'Customer'
        OWNER = 'OWNER', 'Vehicle Owner'
        ADMIN = 'ADMIN', 'Admin'

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=100, default='Morbi')
    driving_license_number = models.CharField(max_length=50, blank=True, null=True)
    aadhaar_number = models.CharField(max_length=20, blank=True, null=True)
    driving_license_front = models.ImageField(upload_to='kyc/dl/', blank=True, null=True)
    aadhaar_card_front = models.ImageField(upload_to='kyc/aadhaar/', blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_kyc_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
