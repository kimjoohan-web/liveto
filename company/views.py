from django.shortcuts import render

# Create your views here.

current_page=""
def index(request):

    current_page="about"
    return render(request, 'company/about.html', {'current_page': current_page})

def about(request):
    current_page="about"
    return render(request, 'company/about.html', {'current_page': current_page})

def business(request):
    current_page="business"
    return render(request, 'company/business.html', {'current_page': current_page})

def clients(request):
    current_page="clients"
    return render(request, 'company/clients.html', {'current_page': current_page})

def works(request):
    current_page="works"
    return render(request, 'company/works.html', {'current_page': current_page})

def location(request):
    current_page="location"   
    return render(request, 'company/location.html', {'current_page': current_page})