# from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('logo_redirect/', views.logo_redirect, name='logo_redirect'),
    path('login_page/', views.login_page, name='login_page'),
    path('signup_page/', views.signup_page, name='signup_page'),
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name ='home'),

    path('image_upload/', views.image_upload, name='image_upload'),
    path('history/', views.history, name='history'),

]
