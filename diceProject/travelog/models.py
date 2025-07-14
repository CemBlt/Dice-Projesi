
from django.db import models
# from django.utils.text import slugify # Slugify otomatik olarak gelmesi için

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Kategori Adı")

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=200, verbose_name="Mekan Adı")
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name="URL Dostu İsim")
    description = models.TextField(blank=True, null=True, verbose_name="Açıklama")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Adres")
    city = models.CharField(max_length=100, verbose_name="Şehir")
    latitude = models.DecimalField(max_digits=19, decimal_places=6, blank=True, null=True, verbose_name="Enlem")
    longitude = models.DecimalField(max_digits=19, decimal_places=6, blank=True, null=True, verbose_name="Boylam")
    location_type = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='locations', verbose_name="Mekan Türü")
    main_photo = models.ImageField(upload_to='location_photos/', blank=True, null=True, verbose_name="Ana Fotoğraf") # Anasayfada kullanılan ana görsel
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")

    class Meta:
        verbose_name = "Mekan"
        verbose_name_plural = "Mekanlar"
        ordering = ['-date_added']

    def __str__(self):
        return f"{self.name} ({self.city})"


class Route(models.Model):
    name = models.CharField(max_length=200, verbose_name="Rota Adı")
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name="URL Dostu İsim")
    description = models.TextField(blank=True, null=True, verbose_name="Açıklama")
    main_image = models.ImageField(upload_to='route_images/', blank=True, null=True, verbose_name="Ana Rota Görseli")
    locations = models.ManyToManyField(Location, blank=True, related_name='routes', verbose_name="Bu Rota İçindeki Mekanlar")
    is_featured = models.BooleanField(default=False, verbose_name="Öne Çıkan Rota (Slider İçin)")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")

    class Meta:
        verbose_name = "Rota"
        verbose_name_plural = "Rotalar"
        ordering = ['-date_created']

    def __str__(self):
        return self.name

# YENİ MODEL: Mekanlara ait ek fotoğraflar ve videolar için
class LocationMedia(models.Model):
    LOCATION_MEDIA_TYPES = (
        ('image', 'Resim'),
        ('video', 'Video'),
    )
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='media_items', verbose_name="Mekan")
    file = models.FileField(upload_to='location_extra_media/', verbose_name="Medya Dosyası") # Hem fotoğraf hem video için FileField
    media_type = models.CharField(max_length=10, choices=LOCATION_MEDIA_TYPES, default='image', verbose_name="Medya Türü")
    caption = models.CharField(max_length=255, blank=True, null=True, verbose_name="Açıklama")
    order = models.IntegerField(default=0, verbose_name="Sıra") # Sıralama için

    class Meta:
        verbose_name = "Mekan Medyası"
        verbose_name_plural = "Mekan Medyaları"
        ordering = ['order', 'id'] # Sıraya ve eklenme sırasına göre sırala

    def __str__(self):
        return f"{self.location.name} - {self.media_type}: {self.caption or self.file.name}"