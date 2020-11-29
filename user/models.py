from django.contrib.gis.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image
from django.utils.text import slugify

# Create your models here.
class Profile(models.Model):
    CHOICES = [('M','Male'),('F','Female')]

    user = models.OneToOneField(User,on_delete = models.CASCADE)
    image = models.ImageField(default = "profile_pics/default.jpg",upload_to = 'profile_pics')
    gender = models.CharField(max_length=1,choices=CHOICES)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    address  = models.CharField(max_length=350)
    postal_code = models.CharField(max_length=10)
    bio = models.CharField(max_length=300,null=True,blank=True,default = "Feeling Great")
    slug = models.SlugField(max_length = 40,unique = True,null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
     
    def save(self,*args, **kwargs):
        u = self.user.username.split("@")[0]+self.user.id
        self.slug = slugify(u)
        super().save()
        # img = Image.open(self.image.path) #there are additional ways to do this
        # if img.height > 300 or img.width > 300:
        #     output_size = (300,300)
        #     img.thumbnail(output_size)
        #     img.save(self.image.path)
