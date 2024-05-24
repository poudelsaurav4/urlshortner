from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import UrlData
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


def details(request):
    list_of_urls = UrlData.objects.order_by('url')
    context = {"list_of_urls":list_of_urls,}
    return render(request,'results.html', context)
    

def redirect_back(request, short_url):
    n_url = UrlData.objects.get(short_url=short_url)
    return redirect(n_url.url)