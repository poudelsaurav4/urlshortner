from django.urls import path
from .views import *
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views


app_name = "urlshort"

urlpatterns = [
    path('', user_login, name='login'),
    path("home/", index, name = "home"),
    path("register/", register, name="register"),
    path("<str:short_url>", redirect_back, name= "redirect"),
    path("details/", details, name = "details"),
    path("/logout/", logout_view, name="logout"),
]