from django.urls import path
from . import views
from django.views.generic.base import RedirectView


app_name = "urlshort"

urlpatterns = [
    path("", views.user_login, name="login"),
    path("home/", views.index, name = "home"),
    path("register/", views.register, name="register"),
    path("<str:short_url>", views.redirect_back, name= "redirect"),
    path("details/", views.details, name = "details"),
    # path("", views.login, name="login"),
]