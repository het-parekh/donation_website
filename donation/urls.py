from . import views 
from django.urls import path


urlpatterns = [
    path('',views.home,name = 'donation-home'),
    path('about/',views.about,name = 'about'),
    #path('/login',views.UserLogin,name = 'login')
]

