import urllib.parse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.vehicles.models import Vehicle, Category
from .models import ContactMessage


def home_view(request):
    featured_vehicles = Vehicle.objects.filter(is_available=True)[:6]
    categories = Category.objects.all()
    context = {
        'featured_vehicles': featured_vehicles,
        'categories': categories,
        'business_name': 'WheelX',
        'phone_number': '9624497998',
        'address': 'Morbi, Gujarat, India',
    }
    return render(request, 'home/index.html', context)


def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        message_text = request.POST.get('message', '').strip()

        if name and phone and message_text:
            # Save message to database
            contact_msg = ContactMessage.objects.create(
                name=name,
                phone=phone,
                message=message_text
            )

            messages.success(
                request,
                f"Thank you {name}! Your message has been saved and is ready to send to WheelX (+91 96244 97998)."
            )
            return redirect('home:contact_success', message_id=contact_msg.id)
        else:
            messages.error(request, "Please fill out all required fields.")
            return redirect('home:contact')

    featured_vehicles = Vehicle.objects.filter(is_available=True)[:6]
    context = {
        'business_name': 'WheelX',
        'phone_number': '9624497998',
        'address': 'Morbi, Gujarat, India',
        'featured_vehicles': featured_vehicles,
    }
    return render(request, 'home/contact.html', context)


def contact_success_view(request, message_id):
    msg_obj = get_object_or_404(ContactMessage, pk=message_id)

    formatted_text = (
        f"Hello WheelX Morbi,\n"
        f"My Name: {msg_obj.name}\n"
        f"Phone: {msg_obj.phone}\n"
        f"Message: {msg_obj.message}"
    )
    encoded_text = urllib.parse.quote(formatted_text)

    # Direct SMS link for native SMS Messenger app to 9624497998
    sms_url = f"sms:+919624497998?body={encoded_text}"

    # WhatsApp link fallback
    whatsapp_url = f"https://wa.me/919624497998?text={encoded_text}"

    context = {
        'contact_msg': msg_obj,
        'sms_url': sms_url,
        'whatsapp_url': whatsapp_url,
        'phone_number': '9624497998',
        'business_name': 'WheelX',
    }
    return render(request, 'home/contact_success.html', context)


def about_view(request):
    context = {
        'business_name': 'WheelX',
        'phone_number': '9624497998',
        'address': 'Morbi, Gujarat, India',
    }
    return render(request, 'home/about.html', context)

