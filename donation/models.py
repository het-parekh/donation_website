from django.contrib.gis.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils.text import slugify

# Create your models here.
def user_directory_path(instance, filename):
# file will be uploaded to MEDIA_ROOT/products/user_<id>/<filename>
    return 'products/user_{0}/{1}/{2}'.format(str(instance.post.author).split("@")[0],instance.post.id,filename)

def main_directory_path(instance,filename):
    return 'products/user_{0}/{1}'.format(str(instance.author).split("@")[0],filename)
class Category(models.Model):
    clothing = sorted(['Sweater','T-shirt','Shirt','Pants','Jeans','Jacket','Shorts','Tops','Leggings','Others'])
    footwear = sorted(['Sandals','Shoes','Slippers',"Women's footwear","Kid's Footwear"])
    books = sorted(['Education','Novels','Biography','Kids','Story'])
    category = sorted(['Clothing','Books','Electronics','Furniture','Footwear'])
    
    name = models.CharField(max_length=20,unique=True)
    slug = models.SlugField(max_length=100,null=True)
    parent = models.ForeignKey('self', null=True,related_name='children',on_delete=models.CASCADE)
    class Meta:
        #enforcing that there can not be two categories under a parent with same slug  
        unique_together = ('slug', 'parent',)    
        verbose_name_plural = "categories"  

    def __str__(self):
        # full_path = [self.name]                  
        # k = self.parent
        # while k is not None:
        #     full_path.append(k.name)
        #     k = k.parent
        # return ' -> '.join(full_path[::-1])
        return self.name

    def save(self,*args, **kwargs):
        self.slug = slugify(self.name)
        super(Category,self).save(*args, **kwargs)


class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE) 
    title = models.CharField(max_length=100,unique=True)
    description = models.CharField(max_length=1000)
    category = models.ForeignKey(Category,null=True,on_delete=models.RESTRICT,related_name='categories')#All posts will be deleted if its category is gone
    
    date = models.DateField(auto_now_add=True)
    note = models.CharField(null = True,blank = True,max_length=100,verbose_name="Special Note/Instruction")
    terms_accepted = models.BooleanField(null=False,blank=False,default=False,verbose_name="I agree to the Terms and Conditions*")
    slug = models.SlugField(max_length=150,unique=True,null=True)
    main_image = models.ImageField(upload_to = main_directory_path,null=True)    
    active = models.BooleanField(default=False,blank = True)

    def __str__(self):
        return f"{self.author} -> {self.title}"
    
    def save(self,*args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        img = Image.open(self.main_image.path)
        if img.height > 500 or img.width > 300:
            output_size = (500,300)
            img.thumbnail(output_size)
            img.save(self.main_image.path)

class Location(models.Model):
    post = models.OneToOneField(Post,null = True, on_delete=models.CASCADE,related_name='user_location')
    location = models.PointField(null = True)
    state = models.CharField(max_length=50,null = True)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)
    approximate = models.BooleanField(default = True)
    def __str__(self):
        return f"{self.id} -> {self.location}"
class ImageUpload(models.Model):
    post = models.ForeignKey(Post ,on_delete=models.CASCADE,related_name='post_img')
    images = models.ImageField(upload_to = user_directory_path,blank=True,null = True)

    def save(self,*args, **kwargs):
        super().save()
        img = Image.open(self.images.path)
        if img.height > 300 or img.width > 150:
            output_size = (300,100)
            img.thumbnail(output_size)
            img.save(self.images.path)

    def __str__(self):
        return f'{self.images.path}'


    