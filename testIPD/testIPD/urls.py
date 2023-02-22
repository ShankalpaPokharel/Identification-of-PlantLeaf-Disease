"""testIPD URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path

from . import views





urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name = 'home'),

    path('upload_image', views.upload_image, name = "upload_image"),
    path('login', views.login, name='login'),
    path('SignUp', views.SignUp, name='SignUp'),
    # path('hsignup', views.handleSignup, name='handleSignup'),
    
    path('camera', views.camera, name='camera'),
    path('capture', views.image_capture_view, name='image_capture_view'),



    path('main/', views.main, name='main'),
    path('signupp', views.signupp, name='signup'),
    path('loginn', views.loginn, name='loginn'),
    # path('main', views.main, name='main'),
    

    path('logout/', views.logout_view, name='logout'),


    # path('404/', views.handler404, name='404'),
    re_path(r'^.*$', views.handler404),
   
]
