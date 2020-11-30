from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from phonenumber_field.formfields import PhoneNumberField

class UserRegisterForm(UserCreationForm ):
    email = forms.EmailField()
    #USERNAME_FIELD='email'
    class Meta:
        model = User
        fields = ['first_name','last_name','email','password1','password2']

class UserProfileForm(forms.ModelForm):
    CHOICES = [('M','Male'),('F','Female')]

    image = forms.ImageField(label='Profile Image',required=False)
    gender = forms.ChoiceField(label='Gender',choices = CHOICES,widget=forms.RadioSelect)
    phone_number = PhoneNumberField(label='Phone Number',widget=forms.NumberInput)
    address = forms.CharField(label='Address' ,max_length=300,widget=forms.Textarea(attrs={'rows':3,'cols':10}))
    postal_code = forms.CharField(label='Postal Code')

    class Meta:
        model = Profile
        fields = ['image','gender','phone_number','address','postal_code']
        exclude=('bio',)

class MyAuthForm(AuthenticationForm):
    error_messages = {
        'invalid_login': (
            ["Credentials either not verified or are invalid. Please Verify your email address if not yet veried."]
        ),
        'inactive':(
            "Please verify your email address and try again"
        )
    }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']
    
class ProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(max_length=300,widget=forms.Textarea(attrs={'rows':5,'cols':10}))
    class Meta:
        model = Profile
        fields = ('image','gender','phone_number','address','postal_code','bio')
        
        
