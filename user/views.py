from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from .forms import UserRegisterForm,UserProfileForm,MyAuthForm,UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.views import LoginView
from .models import Profile
from donation.models import Post
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class MyLoginView(LoginView):
    authentication_form = MyAuthForm
# Create your views here.
def register(request):
    if request.POST.get('register'):
        UserForm = UserRegisterForm(request.POST,)
        ProfileForm = UserProfileForm(request.POST,request.FILES)
        if UserForm.is_valid() and ProfileForm.is_valid():
            #username = form.cleaned_data.get('email')
            #ProfileForm.cleaned_data['phone_number']='+91'+ form.cleaned_data['phone_number']
            user = UserForm.save(commit=False)
            user.username = user.email
            user.save()
            profile = ProfileForm.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request,"Your account has been created successfully ")
            return redirect('login')
    else:
        UserForm = UserRegisterForm()
        ProfileForm = UserProfileForm()
    return render(request,'user/register.html',{'UserForm' :UserForm,'ProfileForm' :ProfileForm})

@login_required
def profile(request,slug):
    profile = get_object_or_404(Profile)
    if request.POST.get("settings"):
        
        UserForm = UserUpdateForm(request.POST,instance=request.user.profile)
        ProfileForm = ProfileUpdateForm(request.POST,request.FILES,instance=request.user)
        if UserForm.is_valid() and ProfileForm.is_valid():
            user = UserForm.save()
            profile = ProfileForm.save()
            messages.success(request,"Your account has been updated successfully ")
            return redirect('profile')
    else:
        UserForm = UserRegisterForm(instance=request.user)
        ProfileForm = UserProfileForm(instance=request.user.profile)

    
    slugs =  get_object_or_404(Profile, slug=slug)
    user_profile = slugs.user
    profile = slugs
    p = Post.objects.filter(author = user_profile)

    page = request.GET.get('page', 1)
    paginator = Paginator(p, 10)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)


    return render(request,'user/profile.html/',{'pages':pages,'user_profile':user_profile,'posts':p,'UserForm' :UserForm,'ProfileForm' :ProfileForm,'profile':slugs})




    # def userupdate_form_valid(self,form):
    #     return form.login(self.request, redirect_url=self.get_success_url())

    # def profileupdate_form_valid(self,form):
    #     return form.signup(self.request, user, self.get_success_url())


    


    


