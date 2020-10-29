from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User



# Create your views here.


def home(request):
    return render(request,'donation/home.html')






