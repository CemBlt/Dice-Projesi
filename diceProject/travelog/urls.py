# travel/urls.py

from django.urls import path
from . import views

app_name = 'travelog'  

urlpatterns = [
    path('', views.home_view, name='home'), 
    path('rotalar/', views.routes_list, name='routes_list'),
    path('rotalar/<slug:slug>/', views.route_detail, name='route_detail'), 
    path('mekanlar/', views.locations_list, name='locations_list'),
    path('mekanlar/<slug:slug>/', views.location_detail, name='location_detail'),  
    path('harita/', views.map_view, name='map'),
    path('iletisim/', views.contact_view, name='contact'),
]