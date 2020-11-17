from django.contrib import admin
from .models import Post,ImageUpload,Category,Location
from django.contrib.gis.admin import OSMGeoAdmin

admin.site.register(Post)
admin.site.register(ImageUpload)
admin.site.register(Category)

# Register your models here.
@admin.register(Location)
class Location(OSMGeoAdmin):
    list_display = ('name', 'location')