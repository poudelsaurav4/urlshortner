from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
# from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings

def register(request):
    if request.method =='POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm password']
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
        else:
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, "Username already taken")
            elif CustomUser.objects.filter(email=email).exists():
                messages.error(request, "Email already registered")
            else:
                CustomUser.objects.create_user(email, password,username= username)
                messages.success(request, "Account created successfully")
                return redirect('urlshort:login')

    return render(request, 'register.html')
    

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                # print("Login successful, redirecting to home")
                return redirect('urlshort:home')
            else:
                messages.error(request, "Invalid email or password")
                # print("Invalid email or password")
        except CustomUser.DoesNotExist:
            messages.error(request, "User with this email does not exist")
            # print("User with this email does not exist")
    return render(request, 'login.html')


@login_required
def index(request):
    # if not request.user.is_authenticated:
        # login_url = f"{settings.LOGIN_URL}?next={request.path}"
        # print(f"Redirecting to: {login_url}") 
        # return redirect(login_url)
        # return redirect(f"{settings.LOGIN_URL}?next={request.path}")

    # else:
    context = {}
    context['username'] = request.user.username
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
                n_url = UrlData.objects.create(url=url, user = request.user)
                short_ur = request.build_absolute_uri() + n_url.short_url
                context['short_ur']= short_ur

    return render(request, 'index.html', context)
# else:
#     return redirect('urlshort:login')

@login_required
def details(request):
    
    host = request.get_host()
    base_url = f"{host}/"
    list_of_urls = UrlData.objects.filter(user=request.user).order_by('url')
    context = {"list_of_urls":list_of_urls,
               "base_url":base_url,
               "username": request.user.username}
    return render(request,'results.html', context)

@login_required
def logout_view(request):
    if request.user.is_authenticated:

        logout(request)
        messages.success(request, "You are successfully logged out")
        return render(request, 'login.html')
    # else:
        # messages.error(request, "you are not logged in yet")
        # redirect('urlshort:home')

def redirect_back(request, short_url):
        n_url = UrlData.objects.get(short_url=short_url)
        return redirect(n_url.url)
