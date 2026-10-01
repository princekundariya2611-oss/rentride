# -*- coding: utf-8 -*-
"""
WheelX Morbi - Fleet Seeder (Local Assets)
All 17 vehicles configured with 100% reliable local static image paths.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.vehicles.models import Category, Vehicle

# Clear old data
Vehicle.objects.all().delete()
Category.objects.all().delete()
print("Cleared old vehicle data.")

# ── CATEGORIES ──────────────────────────────────────────────────────────────────
suv_cat = Category.objects.create(
    name="SUVs & 4x4",
    slug="suvs-4x4",
    icon="fa-truck-monster",
    description="Rugged SUVs perfect for Gujarat highways and family trips."
)
hatchback_cat = Category.objects.create(
    name="Sedans & Hatchbacks",
    slug="sedans-hatchbacks",
    icon="fa-car-side",
    description="Fuel-efficient city cars for Morbi daily commutes."
)
luxury_cat = Category.objects.create(
    name="Luxury & Wedding",
    slug="luxury-wedding",
    icon="fa-gem",
    description="Premium vehicles for weddings, events, and VIP transfers."
)
bike_cat = Category.objects.create(
    name="Bikes & Scooters",
    slug="bikes-scooters",
    icon="fa-motorcycle",
    description="Agile bikes and scooters for city rides and adventures."
)

print("Categories created.")

# ── VEHICLES ────────────────────────────────────────────────────────────────────
vehicles = [

    # ═══════════ MARUTI SUZUKI ═══════════
    {
        "name": "Swift ZXi+ AMT",
        "brand": "Maruti Suzuki",
        "vehicle_type": "CAR",
        "category": hatchback_cat,
        "price_per_day": 1600,
        "price_per_hour": 120,
        "fuel_type": "Petrol",
        "transmission": "Automatic",
        "seats": 5,
        "mileage": "21 kmpl",
        "year": 2024,
        "location": "Morbi, Gujarat",
        "image_url": "/static/image/vehicle/swift.avif",
        "is_available": True, "is_featured": True,
        "rating": 4.8, "review_count": 62,
        "features": "Push-Button Start, SmartPlay Pro+ Touchscreen, Cruise Control, Alloy Wheels, Dual Airbags, ABS+EBD"
    },
    {
        "name": "Baleno Zeta Turbo CVT",
        "brand": "Maruti Suzuki",
        "vehicle_type": "CAR",
        "category": hatchback_cat,
        "price_per_day": 1900,
        "price_per_hour": 145,
        "fuel_type": "Petrol",
        "transmission": "Automatic",
        "seats": 5,
        "mileage": "22 kmpl",
        "year": 2024,
        "location": "Morbi, Gujarat",
        "image_url": "/static/image/vehicle/baleno.avif",
        "is_available": True, "is_featured": True,
        "rating": 4.7, "review_count": 38,
        "features": "HUD Display, 360-Degree Camera, Wireless Charging, Arkamys Sound, LED Headlamps, 6 Airbags"
    },
    {
        "name": "Ertiga ZXi+ CNG",
        "brand": "Maruti Suzuki",
        "vehicle_type": "CAR",
        "category": hatchback_cat,
        "price_per_day": 2200,
        "price_per_hour": 170,
        "fuel_type": "CNG",
        "transmission": "Manual",
        "seats": 7,
        "mileage": "26 kmpl",
        "year": 2023,
        "location": "Morbi, Gujarat",
        "image_url": "/static/image/vehicle/ertiga.jpg",
        "is_available": True, "is_featured": False,
        "rating": 4.6, "review_count": 28,
        "features": "7-Seater, Factory CNG, SmartPlay Studio, Rear AC Vents, Dual Airbags, ABS"
    },

    # ═══════════ HYUNDAI ═══════════
    {
        "name": "Creta SX(O) Sunroof",
        "brand": "Hyundai",
        "vehicle_type": "CAR",
        "category": suv_cat,
        "price_per_day": 3200,
        "price_per_hour": 240,
        "fuel_type": "Petrol",
        "transmission": "Automatic",
        "seats": 5,
        "mileage": "17 kmpl",
        "year": 2024,
        "location": "Morbi, Gujarat",
        "image_url": "/static/image/vehicle/creta.png",
        "is_available": True, "is_featured": True,
        "rating": 4.9, "review_count": 85,
        "features": "Panoramic Sunroof, BOSE 8-Speaker, ADAS, Wireless Charging, 10.25\" Display, 6 Airbags"
    },
    {
        "name": "i20 Asta(O) Turbo DCT",
        "brand": "Hyundai",
        "vehicle_type": "CAR",
        "category": hatchback_cat,
        "price_per_day": 2100,
        "price_per_hour": 160,
        "fuel_type": "Petrol",
        "transmission": "Automatic",
        "seats": 5,
        "mileage": "20 kmpl",
        "year": 2023,
        "location": "Morbi, Gujarat",
        "image_url": "/static/image/vehicle/i20.jpg",
        "is_available": True, "is_featured": True,
        "rating": 4.8, "review_count": 44,
        "features": "Sunroof, BlueLink Connected, Air Purifier, Voice Command, 7 Airbags, Digital Cluster"
    },
    {
        "name": "Venue SX(O) Turbo",
        "brand": "Hyundai",
        "vehicle_type": "CAR",
        "category": suv_cat,
        "price_per_day": 2500,
        "price_per_hour": 190,
        "fuel_type": "Petrol",
        "transmission": "Automatic",
        "seats": 5,
        "mileage": "18 kmpl",
        "year": 2023,
        "location": "Morbi, Gujarat",
        "image_url": "/static/image/vehicle/venue.jpg",
        "is_available": True, "is_featured": False,
        "rating": 4.7, "review_count": 32,
        "features": "BlueLink 60+ Connected Features, Sunroof, 8\" Touchscreen, Wireless Android Auto, 6 Airbags"
    },

    # ═══════════ MAHINDRA ═══════════
    {
        "name": "Thar LX Hard-Top 4WD",
        "brand": "Mahindra",
        "vehicle_type": "CAR",
        "category": suv_cat,
        "price_per_day": 3800,
        "price_per_hour": 290,
        "fuel_type": "Diesel",
        "transmission": "Automatic",
        "seats": 4,
        "mileage": "14 kmpl",
        "year": 2024,
        "location": "Morbi, Gujarat",
        "image_url": "/static/image/vehicle/thar.png",
        "is_available": True, "is_featured": True,
        "rating": 5.0, "review_count": 110,
        "features": "4x4 Low Range Gearbox, Adrenox 17.69cm Display, All-Terrain Tyres, Rear-Wash Wiper, Alloy Wheels"
    },
    {
        "name": "Scorpio-N Z8 Ultimate",
        "brand": "Mahindra",
        "vehicle_type": "CAR",
        "category": suv_cat,
        "price_per_day": 4500,
        "price_per_hour": 340,
        "fuel_type": "Diesel",
        "transmission": "Automatic",
        "seats": 7,
        "mileage": "13 kmpl",
        "year": 2024,
        "location": "Morbi, Gujarat",
        "image_url": "/static/image/vehicle/scorpio.png",
        "is_available": True, "is_featured": True,
        "rating": 4.9, "review_count": 56,
        "features": "12-Speaker Sony 3D Sound, 4x4 Drive Modes, ADAS Suite, Ventilated Seats, Panoramic Sunroof"
    },
    {
        "name": "XUV 700 AX7 Luxury",
        "brand": "Mahindra",
        "vehicle_type": "CAR",
        "category": luxury_cat,
        "price_per_day": 5500,
        "price_per_hour": 420,
        "fuel_type": "Petrol",
        "transmission": "Automatic",
        "seats": 7,
        "mileage": "14 kmpl",
        "year": 2024,
        "location": "Morbi, Gujarat",
        "image_url": "/static/image/vehicle/xuv700.jpg",
        "is_available": True, "is_featured": True,
        "rating": 4.9, "review_count": 37,
        "features": "ADAS Level 2 (18 Features), 12 Harman Speaker, Panoramic Sunroof, Dual HD Displays, 7 Airbags"
    },

    # ═══════════ TOYOTA ═══════════
    {
        "name": "Fortuner Legender 4x4 AT",
        "brand": "Toyota",
        "vehicle_type": "CAR",
        "category": luxury_cat,
        "price_per_day": 7500,
        "price_per_hour": 580,
        "fuel_type": "Diesel",
        "transmission": "Automatic",
        "seats": 7,
        "mileage": "12 kmpl",
        "year": 2024,
        "location": "Morbi, Gujarat",
        "image_url": "/static/image/vehicle/fortuner.png",
        "is_available": True, "is_featured": True,
        "rating": 5.0, "review_count": 30,
        "features": "JBL 11-Speaker Premium Audio, Dual-Zone Climate, 4x4 All-Terrain, Kick-Sensor Boot, Leather Seats"
    },
    {
        "name": "Innova HyCross GX(O) Hybrid",
        "brand": "Toyota",
        "vehicle_type": "CAR",
        "category": luxury_cat,
        "price_per_day": 5500,
        "price_per_hour": 420,
        "fuel_type": "Petrol",
        "transmission": "Automatic",
        "seats": 8,
        "mileage": "21 kmpl",
        "year": 2024,
        "location": "Morbi, Gujarat",
        "image_url": "/static/image/vehicle/hycross.jpg",
        "is_available": True, "is_featured": False,
        "rating": 4.9, "review_count": 21,
        "features": "Self-Charging Hybrid, Panoramic Roof, Captain Seat, ADAS, 9 Airbags, 10.1 Touchscreen"
    },

    # ═══════════ ROYAL ENFIELD ═══════════
    {
        "name": "Classic 350 Signals Edition",
        "brand": "Royal Enfield",
        "vehicle_type": "BIKE",
        "category": bike_cat,
        "price_per_day": 1200,
        "price_per_hour": 90,
        "fuel_type": "Petrol",
        "transmission": "Manual",
        "seats": 2,
        "mileage": "35 kmpl",
        "year": 2023,
        "location": "Morbi, Gujarat",
        "image_url": "/static/image/vehicle/classic350.png",
        "is_available": True, "is_featured": True,
        "rating": 5.0, "review_count": 140,
        "features": "Dual Channel ABS, Tripper GPS Navigation, Electric Start, Chrome Exhaust, Halogen Headlamp"
    },
    {
        "name": "Meteor 350 Supernova",
        "brand": "Royal Enfield",
        "vehicle_type": "BIKE",
        "category": bike_cat,
        "price_per_day": 1400,
        "price_per_hour": 110,
        "fuel_type": "Petrol",
        "transmission": "Manual",
        "seats": 2,
        "mileage": "36 kmpl",
        "year": 2024,
        "location": "Morbi, Gujarat",
        "image_url": "/static/image/vehicle/meteor350_real.jpg",
        "is_available": True, "is_featured": False,
        "rating": 4.8, "review_count": 54,
        "features": "Tripper Navigation Pod, Bluetooth Connectivity, Dual Channel ABS, USB Charging, LED Tail Lamp"
    },

    # ═══════════ HONDA ═══════════
    {
        "name": "Activa 6G DLX",
        "brand": "Honda",
        "vehicle_type": "BIKE",
        "category": bike_cat,
        "price_per_day": 500,
        "price_per_hour": 40,
        "fuel_type": "Petrol",
        "transmission": "Automatic",
        "seats": 2,
        "mileage": "50 kmpl",
        "year": 2024,
        "location": "Morbi, Gujarat",
        "image_url": "/static/image/vehicle/activa_real.jpg",
        "is_available": True, "is_featured": True,
        "rating": 4.7, "review_count": 180,
        "features": "eSP Engine, LED Headlamp, External Fuel Fill, Silent Start, Combi-Brake System, OBD-2"
    },
    {
        "name": "Shine 125 SP",
        "brand": "Honda",
        "vehicle_type": "BIKE",
        "category": bike_cat,
        "price_per_day": 700,
        "price_per_hour": 55,
        "fuel_type": "Petrol",
        "transmission": "Manual",
        "seats": 2,
        "mileage": "60 kmpl",
        "year": 2023,
        "location": "Morbi, Gujarat",
        "image_url": "/static/image/vehicle/shine_real.jpg",
        "is_available": True, "is_featured": False,
        "rating": 4.6, "review_count": 65,
        "features": "PGM-FI Fuel Injection, Disc Brake, LED Headlight, Analogue-Digital Cluster, BS6 OBD-2"
    },

    # ═══════════ TVS ═══════════
    {
        "name": "Apache RTR 160 4V",
        "brand": "TVS",
        "vehicle_type": "BIKE",
        "category": bike_cat,
        "price_per_day": 900,
        "price_per_hour": 70,
        "fuel_type": "Petrol",
        "transmission": "Manual",
        "seats": 2,
        "mileage": "45 kmpl",
        "year": 2024,
        "location": "Morbi, Gujarat",
        "image_url": "/static/image/vehicle/apache_real.jpg",
        "is_available": True, "is_featured": True,
        "rating": 4.8, "review_count": 47,
        "features": "Race Tuned FI, SmartXonnect Bluetooth, Glide-Through Tech, Petal Disc Brakes, LED DRL"
    },
    {
        "name": "Jupiter 125 Classic",
        "brand": "TVS",
        "vehicle_type": "BIKE",
        "category": bike_cat,
        "price_per_day": 550,
        "price_per_hour": 45,
        "fuel_type": "Petrol",
        "transmission": "Automatic",
        "seats": 2,
        "mileage": "52 kmpl",
        "year": 2023,
        "location": "Morbi, Gujarat",
        "image_url": "/static/image/vehicle/jupiter_real.jpg",
        "is_available": True, "is_featured": False,
        "rating": 4.6, "review_count": 39,
        "features": "Sync Brake System, LED Lighting, Under-Seat USB, Digital-Analogue Speedometer, OBD-2"
    },
]

for item in vehicles:
    Vehicle.objects.create(**item)

total = len(vehicles)
print(f"SUCCESS: WheelX fleet seeded with {total} vehicles using 100% LOCAL image assets!")
print("Local asset path: /static/image/vehicle/")
