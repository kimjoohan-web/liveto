
from unittest import case

from django.db import connection
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.utils import timezone
from board.models import board
from board.form import boardForm
from django.shortcuts import render
# Create your views here.
def index(request):
    return render(request, 'biz/biz_webcasting.html')

def webcasting(request):
    return render(request, 'biz/biz_webcasting.html')

def elearning(request):
    return render(request, 'biz/biz_elearning.html')

def relay(request):
    return render(request, 'biz/biz_relay.html')

def station(request):
    return render(request, 'biz/biz_station.html')

def video(request):
    return render(request, 'biz/biz_video.html')

def homepage(request):
    return render(request, 'biz/biz_homepage.html') 

def eseminar(request):
    return render(request, 'biz/biz_eseminar.html')