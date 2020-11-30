from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from .forms import UserRegisterForm,UserProfileForm,MyAuthForm,UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.views import LoginView
from .models import Profile
from donation.models import Post
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import account_activation_token
from django.views import View



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
            user.is_active = False
            user.save()
            profile = ProfileForm.save(commit=False)
            profile.user = user
            profile.save()
            #Start
            current_site = get_current_site(request)
            email_body = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            }

            link = reverse('activate', kwargs={
                            'uidb64': email_body['uid'], 'token': email_body['token']})

            email_subject = 'Activate your account'

            activate_url = 'http://'+current_site.domain+link

            email = EmailMessage(
                email_subject,
                'Hi '+user.username + ', Please the link below to activate your account \n'+activate_url,
                'noreply@semycolon.com',
                [user.email],
            )
            email.send(fail_silently=False)
            #end
            messages.success(request,"Your account has been created successfully. Check your email for verification link. ")
            return redirect('login')
    else:
        UserForm = UserRegisterForm()
        ProfileForm = UserProfileForm()
    return render(request,'user/register.html',{'UserForm' :UserForm,'ProfileForm' :ProfileForm})

class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect('login'+'?message='+'User already activated')

            if not user.is_active:
                user.is_active = True
                user.save()
                messages.success(request, "Your account has been verified successfully. Please login.")
                return redirect('login')

            

            messages.success(request, 'Account activated successfully')
            return redirect('login')

        except Exception as ex:
            pass

        return redirect('login')

@login_required
def profile(request,slug):
    if request.GET.getlist('bookmark_removed[]'):
        post = request.GET.getlist('bookmark_removed[]')
        
        p = Post.objects.filter(id__in = post)
        for i in p:
            i.bookmarked.remove(request.user)
            i.save()
        return redirect(reverse('profile',kwargs = {'slug':request.user.profile.slug}))

    if request.GET.get('bookmark_removed_all'):
        for i in Post.objects.all():
            i.bookmarked.remove(request.user)
            i.save()
        return redirect(reverse('profile',kwargs = {'slug':request.user.profile.slug}))

    if request.GET.getlist('checked_posts[]'):
        post = request.GET.getlist('cheked_posts[]')
        p = Post.objects.filter(id__in = post)
        p.delete()
        return redirect(reverse('profile',kwargs = {'slug':request.user.profile.slug}))

    if request.GET.get('checked_posts_all'):
        p = Post.objects.filter(author == request.user)
        p.delete()
        return redirect(reverse('profile',kwargs = {'slug':request.user.profile.slug}))
        

    if(request.POST.get('profile_del')):
        if (request.POST['profile_del'] == 'CONFIRM'):
            u = User.objects.get(username=request.user.username)
            u.delete()
            messages.success(request, "Your account was deleted successfully")
            return redirect('login')
        else:
            messages.warning(request, "Invalid Confirmation Message")
            return redirect(reverse('profile',kwargs = {'slug':request.user.profile.slug}))

    
    if request.POST.get("settings"):

        ProfileUpdate = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        UserUpdate = UserUpdateForm(request.POST,instance=request.user)
        if UserUpdate.is_valid() and ProfileUpdate.is_valid():
            UserUpdate.save()
            ProfileUpdate.save()
            messages.success(request,"Your account has been updated successfully ")
            return redirect(reverse('donation-home',kwargs = {'slug':request.user.profile.slug}))
    else:
        UserUpdate = UserUpdateForm(instance=request.user)
        ProfileUpdate = ProfileUpdateForm(instance=request.user.profile)

    
    slugs =  get_object_or_404(Profile, slug=slug)
    user_profile = slugs.user

    p = Post.objects.filter(author = user_profile)

    page = request.GET.get('page', 1)
    paginator = Paginator(p, 6)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    # Bookmark pagination
    pb = request.user.bookmark.all()
    page = request.GET.get('b_page', 1)
    paginator = Paginator(pb, 6)
    try:
        pages_bookmark = paginator.page(page)
    except PageNotAnInteger:
        pages_bookmark = paginator.page(1)
    except EmptyPage:
        pages_bookmark = paginator.page(paginator.num_pages)

    

    return render(request,'user/profile.html/',{'pages_bookmark':pages_bookmark,'pages':pages,'user_profile':user_profile,'posts':p,'bookmarked_posts':pb,'UserUpdate' :UserUpdate,'ProfileUpdate' :ProfileUpdate,'profile':slugs})




    # def userupdate_form_valid(self,form):
    #     return form.login(self.request, redirect_url=self.get_success_url())

    # def profileupdate_form_valid(self,form):
    #     return form.signup(self.request, user, self.get_success_url())


    


    


