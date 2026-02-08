from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render

# Create your views here.

def login(request):
    return render(request, 'oliveyoung/login.html')