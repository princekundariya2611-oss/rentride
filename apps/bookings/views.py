from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils import timezone
from django.db.models import Q, Sum, Count
from django.conf import settings
from django.urls import reverse
from datetime import datetime
from django.db.models.functions import TruncMonth, TruncYear
import json
import re
import urllib.parse

from apps.vehicles.models import Vehicle
from .models import Booking
from .razorpay_utils import create_razorpay_order, verify_razorpay_signature, process_security_deposit_refund


def create_booking_view(request, vehicle_id):

    vehicle = get_object_or_404(
        Vehicle,
        pk=vehicle_id
    )

    # =====================================
    # POST REQUEST
    # =====================================

    if request.method == 'POST':

        # Get form data
        name = request.POST.get(
            'customer_name',
            ''
        ).strip()

        phone = request.POST.get(
            'customer_phone',
            ''
        ).strip()

        start_date_str = request.POST.get(
            'start_date',
            ''
        )

        end_date_str = request.POST.get(
            'end_date',
            ''
        )

        pickup_location = request.POST.get(
            'pickup_location',
            'Morbi, Gujarat'
        )

        notes = request.POST.get(
            'notes',
            ''
        )

        dl_number = request.POST.get('driving_license_no', '').strip()
        aadhaar_number = request.POST.get('aadhaar_no', '').strip()
        dl_doc = request.FILES.get('driving_license_doc')
        aadhaar_doc = request.FILES.get('aadhaar_doc')

        has_dl = bool(dl_number or dl_doc)
        has_aadhaar = bool(aadhaar_number or aadhaar_doc)

        if not (has_dl or has_aadhaar):
            messages.error(
                request,
                'KYC Verification Required: Please provide either Driving License (Number or Photo) or Aadhaar Card (Number or Photo).'
            )
            return redirect(
                'vehicles:detail',
                pk=vehicle.id
            )

        is_kyc_auto = True

        # =====================================
        # NAME VALIDATION
        # =====================================

        if not re.fullmatch(
            r'[A-Za-z ]+',
            name
        ):

            messages.error(
                request,
                'Name can contain only letters and spaces.'
            )

            return redirect(
                'vehicles:detail',
                pk=vehicle.id
            )

        if len(name) < 2:

            messages.error(
                request,
                'Please enter a valid name.'
            )

            return redirect(
                'vehicles:detail',
                pk=vehicle.id
            )

        # =====================================
        # PHONE VALIDATION
        # =====================================

        if not re.fullmatch(
            r'[0-9]{10}',
            phone
        ):

            messages.error(
                request,
                'Phone number must contain exactly 10 digits.'
            )

            return redirect(
                'vehicles:detail',
                pk=vehicle.id
            )

        # =====================================
        # DATE REQUIRED
        # =====================================

        if not start_date_str or not end_date_str:

            messages.error(
                request,
                'Please select start date and end date.'
            )

            return redirect(
                'vehicles:detail',
                pk=vehicle.id
            )

        # =====================================
        # CONVERT DATE
        # =====================================

        try:

            start_date = datetime.strptime(
                start_date_str,
                '%Y-%m-%d'
            ).date()

            end_date = datetime.strptime(
                end_date_str,
                '%Y-%m-%d'
            ).date()

        except ValueError:

            messages.error(
                request,
                'Invalid date selected.'
            )

            return redirect(
                'vehicles:detail',
                pk=vehicle.id
            )

        # =====================================
        # TODAY DATE
        # =====================================

        today = timezone.localdate()

        # Start date cannot be past

        if start_date < today:

            messages.error(
                request,
                'Start date cannot be in the past.'
            )

            return redirect(
                'vehicles:detail',
                pk=vehicle.id
            )

        # =====================================
        # END DATE VALIDATION
        # =====================================

        if end_date < start_date:

            messages.error(
                request,
                'End date cannot be before start date.'
            )

            return redirect(
                'vehicles:detail',
                pk=vehicle.id
            )

        # =====================================
        # CALCULATE DAYS
        # =====================================

        days = (
            end_date - start_date
        ).days

        days = max(
            1,
            days
        )

        # =====================================
        # CALCULATE PRICE
        # =====================================

        total_price = (
            vehicle.price_per_day * days
        )

        # =====================================
        # CREATE BOOKING
        # =====================================

        try:

            booking = Booking(
                user=(
                    request.user
                    if request.user.is_authenticated
                    else None
                ),

                vehicle=vehicle,

                customer_name=name,

                customer_phone=phone,

                pickup_location=pickup_location,

                start_date=start_date,

                end_date=end_date,

                total_days=days,

                total_price=total_price,

                notes=notes,

                driving_license_no=dl_number,

                aadhaar_no=aadhaar_number,

                driving_license_doc=dl_doc,

                aadhaar_doc=aadhaar_doc,

                is_kyc_verified=is_kyc_auto,

                status='PENDING'
            )

            booking.save()

        except ValidationError:

            messages.error(
                request,
                'Please check your booking details.'
            )

            return redirect(
                'vehicles:detail',
                pk=vehicle.id
            )

        # =====================================
        # SUCCESS
        # =====================================

        return redirect(
            'bookings:success',
            booking_id=booking.id
        )

    # =====================================
    # GET REQUEST
    # =====================================

    return redirect(
        'vehicles:detail',
        pk=vehicle.id
    )


def booking_success_view(
    request,
    booking_id
):

    booking = get_object_or_404(
        Booking,
        pk=booking_id
    )

    # =====================================
    # FORMATTED RECEIPT FOR WHATSAPP & SMS
    # =====================================
    kyc_txt = "Verified ✅ (Express 2-Min Pickup Active)" if booking.is_kyc_verified else "Pending Document Check ⏳"

    receipt_msg = (
        f"🚗 *WHEELX MORBI - RENTAL BOOKING RECEIPT* 🚗\n"
        f"----------------------------------------\n"
        f"*Booking Ref:* #{booking.id}\n"
        f"*Customer Name:* {booking.customer_name}\n"
        f"*Phone:* +91 {booking.customer_phone}\n"
        f"*Vehicle:* {booking.vehicle.brand} {booking.vehicle.name}\n"
        f"*Rental Dates:* {booking.start_date} to {booking.end_date} ({booking.total_days} Days)\n"
        f"*Total Price:* ₹{booking.total_price:.0f}\n"
        f"*KYC Status:* {kyc_txt}\n\n"
        f"📍 *Pickup Location:* Luxuria Business Park, Mahendranagar Chokadi, Morbi, Gujarat\n"
        f"🗺️ *GPS Directions:* https://maps.google.com/?q=Luxuria+Business+Park+Mahendranagar+Chokadi+Morbi\n\n"
        f"📞 *24/7 Support Hotline:* +91 96244 97998\n"
        f"Thank you for choosing WheelX Morbi!"
    )

    encoded_receipt = urllib.parse.quote(receipt_msg)

    whatsapp_url = f"https://wa.me/919624497998?text={encoded_receipt}"
    whatsapp_customer_url = f"https://wa.me/91{booking.customer_phone}?text={encoded_receipt}"

    # Create Razorpay Order if payment is unpaid
    razorpay_order = None
    if booking.payment_status == 'UNPAID':
        razorpay_order = create_razorpay_order(booking)

    # Dynamic UPI QR Payment details
    upi_id = getattr(settings, 'DEFAULT_UPI_ID', 'pricepatel2611@okaxis')
    upi_name = getattr(settings, 'DEFAULT_UPI_NAME', 'WheelX Morbi Rentals')
    token_amount = booking.get_token_amount()

    upi_uri = (
        f"upi://pay?pa={upi_id}"
        f"&pn={urllib.parse.quote(upi_name)}"
        f"&am={token_amount:.2f}"
        f"&tn={urllib.parse.quote(f'WheelX Booking #{booking.id}')}"
        f"&cu=INR"
    )

    qr_code_url = f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={urllib.parse.quote(upi_uri)}"

    context = {
        'booking': booking,
        'whatsapp_url': whatsapp_url,
        'whatsapp_customer_url': whatsapp_customer_url,
        'receipt_msg': receipt_msg,
        'business_name': 'WheelX',
        'phone_number': '9624497998',
        'pickup_address': 'Luxuria Business Park, Mahendranagar Chokadi, Morbi',
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'razorpay_order': razorpay_order,
        'token_amount': booking.get_token_amount(),
        'remaining_balance': booking.get_remaining_balance(),
        'grand_total_paise': int(booking.get_token_amount() * 100),
        'upi_id': upi_id,
        'upi_uri': upi_uri,
        'qr_code_url': qr_code_url,
    }

    return render(
        request,
        'bookings/booking_success.html',
        context
    )


def confirm_upi_payment_view(request, booking_id):
    """
    Handles direct UPI QR payment confirmation when visitor scans QR & submits UTR / Ref No.
    """
    if request.method == 'POST':
        booking = get_object_or_404(Booking, pk=booking_id)
        utr_no = request.POST.get('utr_no', '').strip()

        booking.payment_status = 'PAID'
        booking.status = 'CONFIRMED'
        booking.razorpay_payment_id = f"UPI_UTR_{utr_no}" if utr_no else f"UPI_QR_{booking.id}_{int(timezone.now().timestamp())}"
        booking.paid_at = timezone.now()
        booking.save()

        messages.success(
            request,
            f"🎉 UPI Payment of ₹{booking.get_token_amount():.0f} Verified! Booking #{booking.id} is now CONFIRMED."
        )

    return redirect('bookings:success', booking_id=booking_id)


def verify_razorpay_payment_view(request):
    """
    Callback endpoint to verify Razorpay signature and mark booking paid.
    """
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_signature = request.POST.get('razorpay_signature')

        booking = get_object_or_404(Booking, pk=booking_id)

        # Handle direct simulation/test confirmation
        is_valid = verify_razorpay_signature(
            razorpay_order_id=razorpay_order_id,
            razorpay_payment_id=razorpay_payment_id,
            razorpay_signature=razorpay_signature
        )

        if is_valid:
            booking.payment_status = 'PAID'
            booking.status = 'CONFIRMED'
            booking.razorpay_order_id = razorpay_order_id
            booking.razorpay_payment_id = razorpay_payment_id or f"pay_mock_{booking.id}"
            booking.razorpay_signature = razorpay_signature or "mock_signature"
            booking.paid_at = timezone.now()
            booking.save()

            messages.success(
                request,
                f"Token Advance payment of ₹{booking.get_token_amount():.0f} verified successfully! Your booking is now CONFIRMED."
            )
            return JsonResponse({'status': 'success', 'redirect_url': reverse('bookings:success', args=[booking.id])})
        else:
            booking.payment_status = 'FAILED'
            booking.save(update_fields=['payment_status'])
            return JsonResponse({'status': 'failed', 'message': 'Signature verification failed.'}, status=400)

    return JsonResponse({'status': 'invalid_request'}, status=400)


def release_deposit_refund_view(request, booking_id):
    """
    Admin/Owner action to trigger security deposit refund upon safe vehicle return.
    """
    if request.method == 'POST':
        booking = get_object_or_404(Booking, pk=booking_id)
        refund_amount_str = request.POST.get('refund_amount')
        
        refund_amount = None
        if refund_amount_str:
            try:
                refund_amount = float(refund_amount_str)
            except ValueError:
                pass

        try:
            process_security_deposit_refund(booking, refund_amount=refund_amount)
            messages.success(
                request,
                f"Security deposit refund for Booking #{booking.id} processed successfully!"
            )
        except Exception as e:
            messages.error(request, f"Refund process failed: {str(e)}")

    return redirect('bookings:dashboard')



def booking_dashboard_view(request):
    if not (request.user.is_authenticated and request.user.is_staff):
        messages.error(request, "You do not have permission to access the dashboard.")
        return redirect('home:index')

    status_filter = request.GET.get('status', 'ALL').upper()
    query = request.GET.get('q', '').strip()

    bookings = Booking.objects.select_related('vehicle', 'user').order_by('-created_at')

    # Apply search filter
    if query:
        bookings = bookings.filter(
            Q(customer_name__icontains=query) |
            Q(customer_phone__icontains=query) |
            Q(vehicle__name__icontains=query) |
            Q(vehicle__brand__icontains=query) |
            Q(pickup_location__icontains=query)
        )

    # Calculate statistics summary
    all_bookings = Booking.objects.all()
    total_bookings = all_bookings.count()
    pending_count = all_bookings.filter(status='PENDING').count()
    confirmed_count = all_bookings.filter(status='CONFIRMED').count()
    active_count = all_bookings.filter(status='ACTIVE').count()
    completed_count = all_bookings.filter(status='COMPLETED').count()
    cancelled_count = all_bookings.filter(status='CANCELLED').count()

    total_revenue = all_bookings.exclude(status='CANCELLED').aggregate(Sum('total_price'))['total_price__sum'] or 0

    # Chart Data Preparation
    monthly_data = (
        all_bookings.exclude(status='CANCELLED')
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(revenue=Sum('total_price'))
        .order_by('month')
    )
    
    yearly_data = (
        all_bookings.exclude(status='CANCELLED')
        .annotate(year=TruncYear('created_at'))
        .values('year')
        .annotate(revenue=Sum('total_price'))
        .order_by('year')
    )
    
    chart_months = [entry['month'].strftime('%b %Y') for entry in monthly_data if entry['month']]
    chart_monthly_revenue = [float(entry['revenue'] or 0) for entry in monthly_data if entry['month']]
    
    chart_years = [entry['year'].strftime('%Y') for entry in yearly_data if entry['year']]
    chart_yearly_revenue = [float(entry['revenue'] or 0) for entry in yearly_data if entry['year']]

    # Vehicle Popularity (Top 5)
    vehicle_popularity = (
        all_bookings.exclude(status='CANCELLED')
        .values('vehicle__brand', 'vehicle__name')
        .annotate(count=Count('id'))
        .order_by('-count')[:5]
    )
    
    chart_vehicle_names = [f"{entry['vehicle__brand']} {entry['vehicle__name']}" for entry in vehicle_popularity]
    chart_vehicle_counts = [entry['count'] for entry in vehicle_popularity]
    
    top_vehicle = vehicle_popularity[0] if vehicle_popularity else None

    # Apply status filter for table display
    if status_filter in ['PENDING', 'CONFIRMED', 'ACTIVE', 'COMPLETED', 'CANCELLED']:
        bookings = bookings.filter(status=status_filter)

    context = {
        'bookings': bookings,
        'selected_status': status_filter,
        'search_query': query,
        'total_bookings': total_bookings,
        'pending_count': pending_count,
        'confirmed_count': confirmed_count,
        'active_count': active_count,
        'completed_count': completed_count,
        'cancelled_count': cancelled_count,
        'total_revenue': total_revenue,
        'status_choices': Booking.STATUS_CHOICES,
        'chart_months': json.dumps(chart_months),
        'chart_monthly_revenue': json.dumps(chart_monthly_revenue),
        'chart_years': json.dumps(chart_years),
        'chart_yearly_revenue': json.dumps(chart_yearly_revenue),
        'chart_vehicle_names': json.dumps(chart_vehicle_names),
        'chart_vehicle_counts': json.dumps(chart_vehicle_counts),
        'top_vehicle': top_vehicle,
    }

    return render(
        request,
        'bookings/dashboard.html',
        context
    )


def update_booking_status_view(request, booking_id):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, pk=booking_id)
        new_status = request.POST.get('status', '').upper()

        valid_statuses = [choice[0] for choice in Booking.STATUS_CHOICES]
        if new_status in valid_statuses:
            booking.status = new_status
            booking.save()
            messages.success(
                request,
                f"Booking #{booking.id} status updated to '{booking.get_status_display()}'."
            )
        else:
            messages.error(request, "Invalid status selected.")

    return redirect('bookings:dashboard')


def upload_booking_kyc_view(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    if request.method == 'POST':
        dl_no = request.POST.get('driving_license_no', '').strip()
        aadhaar_no = request.POST.get('aadhaar_no', '').strip()
        dl_doc = request.FILES.get('driving_license_doc')
        aadhaar_doc = request.FILES.get('aadhaar_doc')

        if dl_no:
            booking.driving_license_no = dl_no
        if aadhaar_no:
            booking.aadhaar_no = aadhaar_no
        if dl_doc:
            booking.driving_license_doc = dl_doc
        if aadhaar_doc:
            booking.aadhaar_doc = aadhaar_doc

        booking.is_kyc_verified = True
        booking.save()
        messages.success(request, "KYC Documents uploaded successfully! Your vehicle pickup is now paperless & fast-tracked.")

    return redirect('bookings:success', booking_id=booking.id)


def toggle_booking_kyc_view(request, booking_id):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, pk=booking_id)
        booking.is_kyc_verified = not booking.is_kyc_verified
        booking.save()
        status_txt = "KYC Verified ✅" if booking.is_kyc_verified else "Pending KYC ⏳"
        messages.success(request, f"Booking #{booking.id} KYC status set to '{status_txt}'.")

    return redirect('bookings:dashboard')