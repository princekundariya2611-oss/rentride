from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('create/<int:vehicle_id>/', views.create_booking_view, name='create'),
    path('success/<int:booking_id>/', views.booking_success_view, name='success'),
    path('verify-payment/', views.verify_razorpay_payment_view, name='verify_payment'),
    path('confirm-upi/<int:booking_id>/', views.confirm_upi_payment_view, name='confirm_upi'),
    path('release-refund/<int:booking_id>/', views.release_deposit_refund_view, name='release_refund'),
    path('dashboard/', views.booking_dashboard_view, name='dashboard'),
    path('status/<int:booking_id>/', views.update_booking_status_view, name='update_status'),
    path('upload-kyc/<int:booking_id>/', views.upload_booking_kyc_view, name='upload_kyc'),
    path('toggle-kyc/<int:booking_id>/', views.toggle_booking_kyc_view, name='toggle_kyc'),
]
