from django.contrib import admin
from .models import Post,ImageUpload,Category,Location
from django.contrib.gis.admin import OSMGeoAdmin

admin.site.register(Category)

class ImageUploadAdmin(admin.StackedInline):
    model = ImageUpload

@admin.register(Location)
class LocationAdmin(OSMGeoAdmin):
    list_display = ('city', 'location')
    point_zoom = 15
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [ImageUploadAdmin]


