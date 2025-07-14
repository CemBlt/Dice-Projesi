# travel/views.py

from django.shortcuts import render, get_object_or_404
from .models import Location, Route
from django.db.models import Count
# from django.conf import settings # Leaflet.js için settings'e gerek yok

def home_view(request):
    featured_routes = Route.objects.filter(is_featured=True).order_by('-date_created')[:5]
    latest_locations = Location.objects.order_by('-date_added')[:9]

    context = {
        'featured_routes': featured_routes,
        'latest_locations': latest_locations,
    }
    return render(request, 'travel/home.html', context)


def routes_list(request):
    all_routes = Route.objects.all().annotate(num_locations=Count('locations')).order_by('name')
    context = {
        'all_routes': all_routes,
        'page_title': 'Tüm Gezi Rotalarımız'
    }
    return render(request, 'travel/routes_list.html', context)


def route_detail(request, slug):
    route = get_object_or_404(Route, slug=slug)
    route_locations = route.locations.all().order_by('name')
    context = {
        'route': route,
        'route_locations': route_locations,
        'page_title': f'{route.name} Rotası'
    }
    return render(request, 'travel/route_detail.html', context)


def locations_list(request):
    all_locations = Location.objects.all().order_by('name')
    context = {
        'all_locations': all_locations,
        'page_title': 'Tüm Mekanlar'
    }
    return render(request, 'travel/locations_list.html', context)

def location_detail(request, slug):
    location = get_object_or_404(Location, slug=slug)
    context = {
        'location': location,
        'page_title': f'{location.name} Detayı'
    }
    return render(request, 'travel/location_detail.html', context)


def map_view(request):
    """Tüm mekanları harita üzerinde gösterir (Leaflet.js ve OpenStreetMap ile)."""
    # Enlem ve boylamı olan mekanları veritabanından çekin
    locations_on_map = Location.objects.filter(latitude__isnull=False, longitude__isnull=False)

    # Haritaya gönderilecek mekan verilerini hazırlayın
    locations_data = []
    for loc in locations_on_map:
        locations_data.append({
            'name': loc.name,
            'lat': float(loc.latitude), # DecimalField'ı float'a çeviriyoruz
            'lng': float(loc.longitude), #
            'description': loc.description,
            'photo_url': loc.main_photo.url if loc.main_photo else '', #
            'slug': loc.slug, # Mekan detay linki için slug'ı ekliyoruz
        })

    context = {
        'page_title': 'Anılarımız Haritası',
        'locations_data': locations_data, # Mekan verilerini şablona gönderin
    }
    return render(request, 'travel/map.html', context)


def contact_view(request):
    return render(request, 'travel/contact.html', {'page_title': 'İletişim'})