from django.shortcuts import render,redirect,get_object_or_404,reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import TemplateView,ListView
from braces.views import JSONResponseMixin,AjaxResponseMixin
from .models import Post,ImageUpload,Category
from .forms import addPostForm,addImagesForm
import json
from django.core import serializers
# Create your views here.


class Home(JSONResponseMixin,AjaxResponseMixin,ListView):
    model = Post
    template_name = 'donation/home.html'
    context_object_name = 'posts'
        # if category:
        #     p = p.filter(category.parent = category)  

    def get_context_data(self, **kwargs):
        context = super(Home,self).get_context_data(**kwargs)
        context["categories"] = Category.objects.filter(parent = None)
        return context

    def get_ajax(self, request, *args, **kwargs):
        data = ''
        if request.GET.get("category"):
            get = request.GET.get("category").strip()
            if get != 'All':
                parent = Category.objects.get(name=get,parent=None)
                c = Category.objects.filter(parent = parent)
                c2 = list(map(str,c))
                data = {'sub_categories':c2}
            else:
                data = {'sub_categories':"ALL"}

        if request.GET.get("display_category"):
            cat = request.GET.get("display_category").strip()
            sub_cats = request.GET.get("display_sub_categories").strip()
            print(cat)
            if cat == 'All':
                posts = Post.objects.all()
            elif sub_cats =='null':
                posts = Post.objects.filter(category__parent = Category.objects.get(name = cat)) 
            else:   
                sub_cats = json.loads(sub_cats)
                print(sub_cats)
                if sub_cats:
                    posts = Post.objects.filter(category__name__in = sub_cats)
                else:
                    posts = Post.objects.all()
            sub_category = []
            category = []
            image = []
            for post in posts:
                sub_category.append(post.category.name)
                category.append(post.category.parent)
                image.append([post.post_img.all()[0].main_image.url])
            
            posts = serializers.serialize("json", posts)
            image_list = list(map(str,image))
            sub_category_list = list(map(str,sub_category))
            category_list = list(map(str,category)) 
            
            data = {'posts':posts,'image':image_list,'sub_category':sub_category_list,'category':category_list}

        return self.render_json_response(data)

def about(request):
    return render(request,'donation/about.html')

global cat
global sub_cat
cat = ''
sub_cat = ''
@login_required
def addPost(request):
    global cat
    global sub_cat
    if request.GET.get('checkboxes') and request.is_ajax():
        cat = request.GET.get('checkboxes')
        c = Category.objects.get(name=cat).children.all()
        c2 = list(map(str,c))
        print(c2)
        return JsonResponse({'sub_categories':c2})

    if request.GET.get('cat') and request.is_ajax():
        sub_cat = request.GET.get('cat')
        cat = request.GET.get('category')   
    #AJAX End------------------------------------------------------------    

    if request.method == 'POST':
        
        addform = addPostForm(request.POST)
        image_form = addImagesForm(request.POST,request.FILES)

        if addform.is_valid and image_form.is_valid(): 
            post_instance = addform.save(commit=False)
            post_instance.author = request.user
            post_instance.save()
   
            pid = post_instance.id
            p = Post.objects.get(id = pid)
            
            parent = Category.objects.get(name=cat,parent=None)
            c = Category.objects.get(name = sub_cat,parent = parent)
            p.category = c
            p.save()

            main_image = request.FILES['main_image']
            images_list = request.FILES.getlist('images') 
            image_instance = ImageUpload(post=p,main_image = main_image)
            image_instance.save()
            for i in images_list:
                image_instance = ImageUpload(post=p,images=i )
                image_instance.save()
            #messages.success(request,"Post Created Successfully")
            return redirect(reverse('donation-home'))
    else:
        addform = addPostForm()
        image_form = addImagesForm()

    return render(request,'donation/addPost.html',{'addform':addform,'image_form':image_form})



                







