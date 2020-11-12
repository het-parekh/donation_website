from django.contrib import admin
from .models import Post,ImageUpload,Category

admin.site.register(Post)
admin.site.register(ImageUpload)
admin.site.register(Category)

# Register your models here.
