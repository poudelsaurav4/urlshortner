from django.urls import path
from . import views

app_name = "urlshort"

urlpatterns = [
    path("", views.index, name = "home"),
    path("<str:short_url>", views.redirect_back, name= "redirect"),
    path("/", views.details, name = "details"),

]