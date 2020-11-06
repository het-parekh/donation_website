from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from .forms import UserRegisterForm,UserProfileForm

# Create your views here.
def register(request):
    if request.POST.get('register'):
        UserForm = UserRegisterForm(request.POST,)
        ProfileForm = UserProfileForm(request.POST,request.FILES)
        if UserForm.is_valid() and ProfileForm.is_valid():
            #username = form.cleaned_data.get('email')
            #ProfileForm.cleaned_data['phone_number']='+91'+ form.cleaned_data['phone_number']
            user = UserForm.save()
            profile = ProfileForm.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request,"Your account has been created successfully ")
            return redirect('login')
    else:
        UserForm = UserRegisterForm()
        ProfileForm = UserProfileForm()
    return render(request,'user/register.html',{'UserForm' :UserForm,'ProfileForm' :ProfileForm})