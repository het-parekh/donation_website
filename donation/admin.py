from django.contrib import admin
from .models import Post,ImageUpload,Category,Location
from django.contrib.gis.admin import OSMGeoAdmin

admin.site.register(Category)

class ImageUploadAdmin(admin.StackedInline):
    model = ImageUpload

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [ImageUploadAdmin]
@admin.register(Location)
class Location(OSMGeoAdmin):
    list_display = ('name', 'location')