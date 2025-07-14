# travel/admin.py

from django.contrib import admin
from .models import Category, Location, Route,LocationMedia

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class LocationMediaInline(admin.TabularInline): # veya admin.StackedInline
    model = LocationMedia
    extra = 1 # Varsayılan olarak 1 boş form gösterir
    fields = ['file', 'media_type', 'caption', 'order'] 

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'location_type', 'date_added')
    list_filter = ('city', 'location_type')
    search_fields = ('name', 'description', 'address', 'city')
    prepopulated_fields = {'slug': ('name',)} # Name yazıldığında slug'ı otomatik doldurur
    inlines = [LocationMediaInline]

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_featured', 'date_created')
    list_filter = ('is_featured',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('locations',) # ManyToMany alanı için daha güzel bir arayüz sağlar