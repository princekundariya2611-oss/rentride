from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Vehicle, Category


def vehicle_list_view(request):
    vehicles = Vehicle.objects.filter(is_available=True)
    categories = Category.objects.all()

    # Search filter
    search_query = request.GET.get('q', '')
    if search_query:
        vehicles = vehicles.filter(
            Q(name__icontains=search_query) |
            Q(brand__icontains=search_query) |
            Q(location__icontains=search_query)
        )

    # Category filter
    category_slug = request.GET.get('category', '')
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        vehicles = vehicles.filter(category=selected_category)

    # Vehicle type filter (CAR / BIKE)
    vehicle_type = request.GET.get('type', '')
    if vehicle_type:
        vehicles = vehicles.filter(vehicle_type=vehicle_type.upper())

    # Sorting
    sort_by = request.GET.get('sort', '')
    if sort_by == 'price_low':
        vehicles = vehicles.order_by('price_per_day')
    elif sort_by == 'price_high':
        vehicles = vehicles.order_by('-price_per_day')
    elif sort_by == 'rating':
        vehicles = vehicles.order_by('-rating')

    context = {
        'vehicles': vehicles,
        'categories': categories,
        'selected_category': selected_category,
        'search_query': search_query,
        'vehicle_type': vehicle_type,
        'sort_by': sort_by,
        'business_name': 'WheelX',
        'phone_number': '9624497998',
    }
    return render(request, 'vehicles/vehicle_list.html', context)


def vehicle_detail_view(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    related_vehicles = Vehicle.objects.filter(category=vehicle.category).exclude(pk=vehicle.pk)[:3]
    
    context = {
        'vehicle': vehicle,
        'related_vehicles': related_vehicles,
        'business_name': 'WheelX',
        'phone_number': '9624497998',
    }
    return render(request, 'vehicles/vehicle_detail.html', context)
