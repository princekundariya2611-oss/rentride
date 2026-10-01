from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.vehicles.models import Vehicle
import re


class Booking(models.Model):

    STATUS_CHOICES = (
        ('PENDING', 'Pending Confirmation'),
        ('CONFIRMED', 'Confirmed'),
        ('ACTIVE', 'Ongoing Rental'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )

    PAYMENT_STATUS_CHOICES = (
        ('UNPAID', 'Unpaid'),
        ('PAID', 'Paid & Confirmed'),
        ('FAILED', 'Payment Failed'),
        ('REFUNDED', 'Security Deposit Refunded'),
    )

    REFUND_STATUS_CHOICES = (
        ('HELD', 'Security Deposit Held'),
        ('RELEASED', 'Refund Released'),
        ('DEDUCTED', 'Deducted for Damage/Late'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bookings'
    )

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    customer_name = models.CharField(
        max_length=100
    )

    customer_phone = models.CharField(
        max_length=10
    )

    pickup_location = models.CharField(
        max_length=100,
        default='Morbi, Gujarat'
    )

    start_date = models.DateField()

    end_date = models.DateField()

    total_days = models.PositiveIntegerField(
        default=1
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    security_deposit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1000.00,
        help_text='Refundable Security Deposit'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='UNPAID'
    )

    refund_status = models.CharField(
        max_length=20,
        choices=REFUND_STATUS_CHOICES,
        default='HELD'
    )

    razorpay_order_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    razorpay_payment_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    razorpay_signature = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    paid_at = models.DateTimeField(
        blank=True,
        null=True
    )

    refunded_at = models.DateTimeField(
        blank=True,
        null=True
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    driving_license_no = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    aadhaar_no = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    driving_license_doc = models.ImageField(
        upload_to='bookings/kyc/dl/',
        blank=True,
        null=True
    )

    aadhaar_doc = models.ImageField(
        upload_to='bookings/kyc/aadhaar/',
        blank=True,
        null=True
    )

    is_kyc_verified = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def clean(self):

        # =====================================
        # CUSTOMER NAME VALIDATION
        # =====================================

        if self.customer_name:

            name = self.customer_name.strip()

            if not re.fullmatch(r'[A-Za-z ]+', name):
                raise ValidationError({
                    'customer_name':
                    'Name can contain only letters and spaces.'
                })

            if len(name) < 2:
                raise ValidationError({
                    'customer_name':
                    'Please enter a valid name.'
                })

        # =====================================
        # PHONE VALIDATION
        # =====================================

        if self.customer_phone:

            phone = self.customer_phone.strip()

            if not re.fullmatch(r'[0-9]{10}', phone):
                raise ValidationError({
                    'customer_phone':
                    'Phone number must contain exactly 10 digits.'
                })

        # =====================================
        # DATE VALIDATION
        # =====================================

        today = timezone.localdate()

        if not self.pk and self.start_date:

            if self.start_date < today:
                raise ValidationError({
                    'start_date':
                    'Start date cannot be in the past.'
                })

        if self.start_date and self.end_date:

            if self.end_date < self.start_date:
                raise ValidationError({
                    'end_date':
                    'End date cannot be before start date.'
                })

    def save(self, *args, **kwargs):
        # Calculate rental days
        if self.start_date and self.end_date:
            days = (
                self.end_date - self.start_date
            ).days
            self.total_days = max(1, days)

        # Calculate price
        if self.vehicle and self.vehicle.price_per_day:
            self.total_price = (
                self.vehicle.price_per_day *
                self.total_days
            )

        # Run validation before saving
        self.full_clean()

        super().save(*args, **kwargs)

    TOKEN_AMOUNT_INR = 1000.00

    def get_grand_total(self):
        """Total amount payable (Rental Price + Security Deposit)"""
        total = self.total_price if self.total_price is not None else 0
        deposit = self.security_deposit if self.security_deposit is not None else 1000.00
        return float(total) + float(deposit)

    def get_token_amount(self):
        """Token advance amount required online (₹1000 to reserve vehicle)"""
        return min(self.TOKEN_AMOUNT_INR, self.get_grand_total())

    def get_remaining_balance(self):
        """Remaining balance payable at pickup in Morbi"""
        return self.get_grand_total() - self.get_token_amount()

    def __str__(self):

        return (
            f"Booking #{self.id} - "
            f"{self.customer_name} "
            f"({self.vehicle.name})"
        )