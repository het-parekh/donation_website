from . import views 
from django.urls import path


urlpatterns = [
    path('',views.Home.as_view(),name = 'donation-home'),
    path('about/',views.about,name = 'about'),
    path('addPost/',views.addPost,name = 'addPost'),
    path('post_detail/<slug:slug>',views.Post_Detail.as_view(template_name = 'donation/post_detail.html'),name = 'post-detail'),
    #path('/login',views.UserLogin,name = 'login')
]

