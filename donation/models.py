from django.db import models
from django.contrib.auth.models import User
import operator
from PIL import Image
# Create your models here.
def user_directory_path(instance, filename):
# file will be uploaded to MEDIA_ROOT/products/user_<id>/<filename>
    return 'products/user_{0}/{1}/{2}'.format(str(instance.post.author).split("@")[0],instance.post.id,filename)

class Post(models.Model):
    CHOICES = sorted([('Sweater','Sweater'),('T_shirt','T-shirt'),('Shirt','Shirt'),('Pants','Pants'),
                ('Jeans','Jeans'),('Homeware','Homeware'), ('Jacket','Jacket'),('Books','Books'),
                ('Electronics','Electronics'),('Furniture','Furniture'),('Shorts','Shorts')],key=operator.itemgetter(0))
    
    author = models.ForeignKey(User,on_delete=models.CASCADE) 
    title = models.CharField(max_length=101,)
    description = models.CharField(max_length=1000)
    category = models.CharField(max_length=30,choices=CHOICES)


            
class ImageUpload(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='_post')
    images = models.ImageField(upload_to = user_directory_path,blank=True)

    def save(self,*args, **kwargs):
        super().save()
        print(self.images)
        img = Image.open(self.images.path)
        if img.height > 800 or img.width > 500:
            output_size = (500,500)
            img.thumbnail(output_size)
            img.save(self.images.path)
    
    def delete(self, using=None, keep_parents=False):
        self.images.delete()
        super().delete()

    
