from django.shortcuts import render,redirect,get_object_or_404,reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import TemplateView,ListView,DetailView
from braces.views import JSONResponseMixin,AjaxResponseMixin
from .models import Post,ImageUpload,Category,Location
from .forms import addPostForm,addImagesForm,addLocationForm
import json
from django.core import serializers
from django.contrib.gis.geoip2 import GeoIP2
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
import time
from django.conf import settings
# Create your views here.

def geoIP(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    g = GeoIP2()
    location = g.city(ip)
    latitude = location['latitude']
    longitude = location["longitude"]
    city = location["city"]
    postal_code = location["postal_code"]
    state_code = location["region"]
    STATE_CHOICES = (('KA', 'Karnataka'), ('AP', 'Andhra Pradesh'), ('KL', 'Kerala'), ('TN', 'Tamil Nadu'), ('MH', 'Maharashtra'), ('UP', 'Uttar Pradesh'), ('GA', 'Goa'), ('GJ', 'Gujarat'), ('RJ', 'Rajasthan'), ('HP', 'Himachal Pradesh'), ('JK', 'Jammu and Kashmir'), ('TG', 'Telangana'), ('AR', 'Arunachal Pradesh'), ('AS', 'Assam'), ('BR', 'Bihar'), ('CG', 'Chattisgarh'), ('HR', 'Haryana'), ('JH', 'Jharkhand'), ('MP', 'Madhya Pradesh'), ('MN', 'Manipur'), ('ML', 'Meghalaya'), ('MZ', 'Mizoram'), ('NL', 'Nagaland'), ('OR', 'Orissa'), ('PB', 'Punjab'), ('SK', 'Sikkim'), ('TR', 'Tripura'), ('UA', 'Uttarakhand'), ('WB', 'West Bengal'), ('AN', 'Andaman and Nicobar'), ('CH', 'Chandigarh'), ('DN', 'Dadra and Nagar Haveli'), ('DD', 'Daman and Diu'), ('DL', 'Delhi'), ('LD', 'Lakshadweep'), ('PY', 'Pondicherry'))
    state = [i for  i  in STATE_CHOICES if i[0] == state_code][0][1]
    return [latitude,longitude,city,postal_code,state]

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
    
    geo_permit = False
    def get_ajax(self, request, *args, **kwargs):
        data = ''
        search=''
        geo_permit = False
        current_position = ''
    
        if request.GET.get("search"):
            search = request.GET.get("search")
        if request.GET.get("category"):
            get = request.GET.get("category").strip()
            if get != 'All':
                parent = Category.objects.get(name=get,parent=None)
                c = Category.objects.filter(parent = parent)
                c2 = list(map(str,c))
                data = {'sub_categories':c2}
            else:
                data = {'sub_categories':"ALL"}

        if request.GET.get("display_sub_categories"):
            cat = request.GET.get("display_category").strip()
            sub_cats = request.GET.get("display_sub_categories").strip()
            geo = request.GET.getlist("geo[]")
            if geo and geo[0] != 'geo_denied':
                current_position = GEOSGeometry(f'POINT ({geo[1]} {geo[0]})', srid=4326)
                geo_permit = True
            else:
                geoip = geoIP(request)
                current_position = GEOSGeometry(f'POINT ({geoip[1]} {geoip[0]})', srid=4326)
                geo_permit = False

            if cat == 'All':
                posts = Post.objects.all()
            elif sub_cats == "null":
                posts = Post.objects.filter(category__parent = Category.objects.get(name = cat)) 
            else:   
                sub_cats = json.loads(sub_cats)
                if sub_cats:
                    posts = Post.objects.filter(category__name__in = sub_cats)
                else:
                    posts = Post.objects.all()
            posts = posts.filter(title__icontains = search)
            
            if current_position:
                posts = posts.filter(user_location__location__distance_lte = (current_position,D(m=20000))).annotate(distance=Distance("user_location__location", current_position)).order_by("distance")   #10km      
            sub_category = []
            category = []
            distance = []
            for post in posts:
                sub_category.append(post.category.name)
                category.append(post.category.parent)
                if(geo_permit == True):
                    distance.append(current_position.distance(post.user_location.location)*100)
            
            posts = serializers.serialize("json", posts)
            sub_category_list = list(map(str,sub_category))
            category_list = list(map(str,category)) 
            data = {'posts':posts,'sub_category':sub_category_list,'category':category_list,'distance':sorted(distance),'media':settings.MEDIA_URL}

        return self.render_json_response(data)


def about(request):
    return render(request,'donation/about.html')

global cat
global sub_cat
cat = ''
sub_cat = ''
geo_details_list = []
@login_required
def addPost(request):
    global cat
    global sub_cat
    global geo_details_list #['latitude','longitude','city','state','zipcode','Approx']
    
    if request.GET.get('checkboxes') and request.is_ajax():
        cat = request.GET.get('checkboxes')
        c = Category.objects.get(name=cat).children.all()
        c2 = list(map(str,c))
        return JsonResponse({'sub_categories':c2})

    if request.GET.get('cat') and request.is_ajax():
        sub_cat = request.GET.get('cat')
        cat = request.GET.get('category')   
    
    if request.GET.getlist("geo[]"):
        geo = request.GET.getlist("geo[]")
        geo_details_list = geoIP(request)
        geo_details_list[0] = geo[0]
        geo_details_list[1] = geo[1]
        geo_details_list.append(False)
        return JsonResponse({'address':geo_details_list})

    elif request.GET.get('geo_denied'):
        geo_details_list = geoIP(request)
        geo_details_list.append(True)
        return JsonResponse({'address':geo_details_list})

    #AJAX End------------------------------------------------------------    

    if request.method == 'POST':
        
        addform = addPostForm(request.POST,request.FILES)
        image_form = addImagesForm(request.POST,request.FILES)
        location_form  = addLocationForm(request.POST)

        if addform.is_valid and image_form.is_valid() and location_form.is_valid(): 
            post_instance = addform.save(commit=False)
            post_instance.author = request.user
            post_instance.save()

            pid = post_instance.id
            p = Post.objects.get(id = pid)
            
            parent = Category.objects.get(name=cat,parent=None)
            c = Category.objects.get(name = sub_cat,parent = parent)
            p.category = c
            p.save()

            images_list = request.FILES.getlist('images') 
            for i in images_list:
                image_instance = ImageUpload(post=p,images=i )
                image_instance.save()
            #messages.success(request,"Post Created Successfully")
            print(geo_details_list)
            current_position = GEOSGeometry(f'POINT ({geo_details_list[1]} {geo_details_list[0]})', srid=4326) 
            locate = location_form.save(commit=False)
            locate.post = p
            locate.save()
            locate = Location.objects.get(post = p)
            locate.approximate = geo_details_list[5]
            locate.location = current_position
            locate.save()

            return redirect(reverse('post-detail' ,kwargs={'slug':p.slug}))
    else:
        location_form  = addLocationForm()
        addform = addPostForm()
        image_form = addImagesForm()

    return render(request,'donation/addPost.html',{'addform':addform,'image_form':image_form,'location_form':location_form})


class Post_Detail(DetailView):
    model = Post
    slug_url_kwarg = 'slug'
    slug_field = 'slug'
    context_object_name = 'post'
    template_name = 'donation/post_detail.html'

    def get(self, request, *args, **kwargs):
        if self.request.GET.get('Key'):
            self.object = self.get_object()
            if self.object.author == self.request.user:
                self.object.delete()
                return(redirect('/')) 

        return super().get(request, *args, **kwargs)
    


    
# def post_detail(request,slug):
#     p = get_object_or_404(Post,slug=slug)
#     return render(request,'donation/post_detail.html',{"slug":p})

                







