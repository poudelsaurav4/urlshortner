from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404
from .models import *
# import message

from django.contrib.auth import authenticate,login
# Create your views here.
def index(request):
    context = {}
    if request.method == "POST":
        url  = request.POST['url']

        if url:        
            existing_url = UrlData.objects.filter(url=url).first()
            if existing_url:
                short_ur = request.build_absolute_uri()+existing_url.short_url
                context['short_ur']= short_ur

        # if url in UrlData.objects.filter(url=url):
        #     short_ur = request.build_absolute_uri()+url.short_url
            else:
                n_url = UrlData.objects.create(url=url)
                short_ur = request.build_absolute_uri() + n_url.short_url
                context['short_ur']= short_ur

    return render(request, 'index.html', context)

def register(request):
    errors={}
    if request.method == "POST":
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm password')
        # import ipdb;ipdb.set_trace()  
        # breakpoint()
        if not email:
            errors['empty_email'] = "email should not be empty"

        elif not username:
            errors['empty_username'] = "username should not be empty"

        elif not password:
            errors['empty_password'] = "password should not be empty"

        elif password != confirm_password:
            errors['confirm_password'] = "Passwords do not match"
        
        else:
            if RegisterUser.objects.filter(username=username).exists():
                errors['username'] = "Username already taken"

            if RegisterUser.objects.filter(email=email).exists():
                errors['email'] = "Email already registered"


        if not errors:
            RegisterUser.objects.create(email=email, username=username, password=password)
            return redirect('urlshort:login')


    return render(request, 'register.html', {'errors': errors})


def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = RegisterUser.objects.filter(email=email).first()
        # user = authenticate(email=email, password=password)
        password_user = RegisterUser.objects.filter(password=password).first()  
        if user is not None and password_user:

            # login(request, user)
            return redirect('urlshort:home')

        else:
            error= 'invalid email'
            return render(request, 'login.html', {'error':error})

    return render(request, 'login.html')


def details(request):
    
    host = request.get_host()
    base_url = f"{host}/"
    list_of_urls = UrlData.objects.order_by('url')
    context = {"list_of_urls":list_of_urls,
               "base_url":base_url}
    return render(request,'results.html', context)
    
def redirect_back(request, short_url):
        n_url = UrlData.objects.get(short_url=short_url)
        return redirect(n_url.url)
    
