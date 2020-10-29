from django.shortcuts import render,get_object_or_404

# Create your views here.
def register(request):
    return render(request,'user/register.html')