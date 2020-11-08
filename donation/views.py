from django.shortcuts import render,redirect,get_object_or_404,reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post,ImageUpload
from .forms import addPostForm,addImagesForm
# Create your views here.


def home(request):
    return render(request,'donation/home.html')

def about(request):
    return render(request,'donation/about.html')

@login_required
def addPost(request):
    if request.method == 'POST':
        addform = addPostForm(request.POST)
        image_form = addImagesForm(request.POST,request.FILES)
        if addform.is_valid and image_form.is_valid():
            post_instance = addform.save(commit=False)
            post_instance.author = request.user
            post_instance.save()
            images_list = request.FILES.getlist('images') 
            print(images_list)
            for i in images_list:
                image_instance = ImageUpload(post=post_instance,images=i )
                image_instance.save()
            return redirect(reverse('donation-home'))
    else:
        addform = addPostForm()
        image_form = addImagesForm()

    return render(request,'donation/addPost.html',{'addform':addform,'image_form':image_form})



                







