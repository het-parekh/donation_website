from . import views 
from django.urls import path


urlpatterns = [
    path('',views.Home.as_view(),name = 'donation-home'),
    path('about/',views.about,name = 'about'),
    path('addPost/',views.addPost,name = 'addPost'),
    #path('/login',views.UserLogin,name = 'login')
]

