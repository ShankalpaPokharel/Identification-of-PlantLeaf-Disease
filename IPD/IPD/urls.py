"""
URL configuration for IPD project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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



# from django.contrib import admin
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', views.index, name='index'),
#     path('logo_redirect/', views.logo_redirect, name='logo_redirect'),
#     path('login_page/', views.login_page, name='login_page'),
#     path('signup_page/', views.signup_page, name='signup_page'),
#     path('signup/', views.signup, name="signup"),
#     path('login/', views.login, name='login'),
#     path('logout/', views.logout_view, name='logout'),
#     path('home/', views.home, name ='home'),

#     path('image_upload/', views.image_upload, name='image_upload'),

# ]


from django.contrib import admin
from django.urls import include
from django.urls import path

from django.conf.urls.static import static
from django.conf import settings

from disease_detection.views import page_not_found_view


from django.views.static import serve


# from django.conf.urls import url

# from django.conf import settings

# from django.views.static import serve

from django.urls import re_path

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    re_path(r'^model_dict/(?P<path>.*)$', serve,{'document_root': settings.MODEL_ROOT}),





    path('admin/', admin.site.urls),
    path('', include('disease_detection.urls')),

    



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.conf.urls import handler404

handler404 = 'disease_detection.views.page_not_found_view'


# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)