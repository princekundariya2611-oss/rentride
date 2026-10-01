# 🚗 WheelX — Vehicle Rentals Morbi

A Django-based vehicle rental web application for Morbi, Gujarat.

## Project Structure

```
RENTRIDE/
├── apps/
│   ├── accounts/       # CustomUser model (role-based: Customer, Owner, Admin)
│   ├── bookings/       # Booking model, views, and URLs
│   ├── home/           # Home, About, Contact views
│   └── vehicles/       # Vehicle + Category models, fleet views
├── config/
│   ├── settings.py     # Django settings
│   ├── urls.py         # Root URL configuration
│   ├── wsgi.py
│   └── asgi.py
├── static/
│   ├── css/
│   │   └── style.css   # Main stylesheet
│   ├── js/
│   │   └── main.js     # Main JavaScript
│   ├── fonts/          # Poppins, Roboto fonts
│   ├── image/
│   │   ├── banners/    # Hero banner images
│   │   ├── logo/       # Site logo
│   │   ├── users/      # Default user avatar
│   │   └── vehicle/    # Vehicle photos (real JPG/PNG/AVIF)
│   └── vendor/         # Bootstrap, FontAwesome, jQuery, AOS, Owl Carousel
├── templates/
│   ├── base.html       # Base layout template
│   ├── accounts/
│   │   └── login.html
│   ├── bookings/
│   │   └── booking_success.html
│   ├── home/
│   │   ├── index.html
│   │   ├── about.html
│   │   └── contact.html
│   └── vehicles/
│       ├── vehicle_list.html
│       └── vehicle_detail.html
├── db.sqlite3          # SQLite database
├── manage.py
└── seed_wheelx.py      # Fleet seeder script
```

## Quick Start

```bash
# Install dependencies
pip install django pillow whitenoise

# Run migrations
python manage.py migrate

# Seed the fleet (17 vehicles)
python seed_wheelx.py

# Start development server
python manage.py runserver
```

## Fleet (17 Vehicles)

| Brand | Model | Category |
|---|---|---|
| Maruti Suzuki | Swift ZXi+ AMT | Hatchback |
| Maruti Suzuki | Baleno Zeta Turbo CVT | Hatchback |
| Maruti Suzuki | Ertiga ZXi+ CNG | Hatchback |
| Hyundai | Creta SX(O) Sunroof | SUV |
| Hyundai | i20 Asta(O) Turbo DCT | Hatchback |
| Hyundai | Venue SX(O) Turbo | SUV |
| Mahindra | Thar LX Hard-Top 4WD | SUV |
| Mahindra | Scorpio-N Z8 Ultimate | SUV |
| Mahindra | XUV 700 AX7 Luxury | Luxury |
| Toyota | Fortuner Legender 4x4 AT | Luxury |
| Toyota | Innova HyCross GX(O) Hybrid | Luxury |
| Royal Enfield | Classic 350 Signals Edition | Bike |
| Royal Enfield | Meteor 350 Supernova | Bike |
| Honda | Activa 6G DLX | Scooter |
| Honda | Shine 125 SP | Bike |
| TVS | Apache RTR 160 4V | Bike |
| TVS | Jupiter 125 Classic | Scooter |
